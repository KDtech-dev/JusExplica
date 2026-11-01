<?php

namespace App\Services\Whatsapp;

use App\Models\WhatsappConversation;
use App\Models\WhatsappMessage;

class ConversationService
{
    public function findOrCreate(string $phone): WhatsappConversation
    {
        return WhatsappConversation::firstOrCreate(
            ['phone' => $phone],
            ['state' => 'inicio']
        );
    }

    public function incomingExists(
        WhatsappConversation $conversation,
        string $messageId
    ): bool {
        return $conversation->messages()
            ->where('message_id', $messageId)
            ->exists();
    }

    public function registerIncoming(
        WhatsappConversation $conversation,
        array $payload
    ): WhatsappMessage {
        return $conversation->messages()->create([
            'message_id' => $payload['message_id'],
            'direction' => 'incoming',
            'type' => $payload['type'],
            'content' => $payload['content'],
        ]);
    }

    public function registerOutgoing(
        WhatsappConversation $conversation,
        string $messageId,
        string $content
    ): WhatsappMessage {
        return $conversation->messages()->create([
            'message_id' => $messageId,
            'direction' => 'outgoing',
            'type' => 'text',
            'content' => $content,
        ]);
    }

    public function updateState(
        WhatsappConversation $conversation,
        string $state,
        ?string $processNumber = null,
        bool $clearProcessNumber = false
    ): void {
        $data = [
            'state' => $state,
            'last_interaction_at' => now(),
        ];

        if ($processNumber !== null) {
            $data['process_number'] = $processNumber;
        }

        if ($clearProcessNumber) {
            $data['process_number'] = null;
        }

        $conversation->update($data);
    }
}