<?php

namespace App\Services\Whatsapp;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class WhatsappMessageService
{
    public function __construct(
        private ConversationService $conversationService
    ) {}

    public function process(array $payload): array
    {
        return DB::transaction(function () use ($payload) {
            $conversation = $this->conversationService->findOrCreate(
                $payload['sender']
            );

            // Evita processar mensagens duplicadas.
            if (
                $this->conversationService->incomingExists(
                    $conversation,
                    $payload['message_id']
                )
            ) {
                return [
                    'reply' => null,
                    'duplicate' => true,
                ];
            }

            $this->conversationService->registerIncoming(
                $conversation,
                $payload
            );

            $content = trim($payload['content']);

            $reply = match ($conversation->state) {
                'inicio' => $this->handleStart($conversation),

                'aguardando_identificador' =>
                    $this->handleProcessNumber($conversation, $content),

                'confirmando_identificador' =>
                    $this->handleConfirmation($conversation, $content),

                'processo_confirmado' =>
                    $this->handleConfirmedProcess(),

                default => $this->handleStart($conversation),
            };

            $this->conversationService->registerOutgoing(
                $conversation,
                'outgoing-' . Str::uuid(),
                $reply
            );

            return [
                'reply' => $reply,
                'duplicate' => false,
            ];
        });
    }

    private function handleStart($conversation): string
    {
        $this->conversationService->updateState(
            $conversation,
            'aguardando_identificador'
        );

        return 'Olá! Sou o JusExplica. Para começar, informe o número do processo que deseja consultar.';
    }

    private function handleProcessNumber(
        $conversation,
        string $content
    ): string {
        $pattern = '/\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b/';

        if (!preg_match($pattern, $content, $matches)) {
            return 'Não consegui identificar um número de processo válido no formato CNJ. Por favor, envie novamente.';
        }

        $processNumber = $matches[0];

        $this->conversationService->updateState(
            $conversation,
            'confirmando_identificador',
            $processNumber
        );

        return "Identifiquei o processo {$processNumber}. Esse é o processo que deseja consultar? Responda SIM ou NÃO.";
    }

    private function handleConfirmation(
        $conversation,
        string $content
    ): string {
        $answer = mb_strtolower(trim($content));

        if (in_array($answer, ['sim', 's', 'confirmo'], true)) {
            $this->conversationService->updateState(
                $conversation,
                'processo_confirmado'
            );

            return "Número do processo confirmado: {$conversation->process_number}.\n\nA próxima etapa será integrar a consulta processual para buscar as movimentações e explicá-las em linguagem simples.";
        }

        if (in_array($answer, ['não', 'nao', 'n'], true)) {
            $this->conversationService->updateState(
                $conversation,
                'aguardando_identificador',
                clearProcessNumber: true
            );

            return 'Sem problemas! Informe novamente o número do processo que deseja consultar.';
        }

        return 'Não consegui entender sua resposta. Por favor, responda SIM para confirmar ou NÃO para informar outro número.';
    }

    private function handleConfirmedProcess(): string
    {
        return 'O número do processo já foi confirmado. A integração com a consulta processual ainda está em desenvolvimento.';
    }
}