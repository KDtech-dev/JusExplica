<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\Whatsapp\ReceiveMessageRequest;
use App\Services\ResponseService;
use App\Services\Whatsapp\WhatsappMessageService;
use Illuminate\Http\JsonResponse;

class WhatsappController extends Controller
{
    public function receive(
        ReceiveMessageRequest $request,
        WhatsappMessageService $service,
        ResponseService $responseService
    ): JsonResponse {
        $result = $service->process($request->validated());

        return $responseService->success(
            'Mensagem processada com sucesso.',
            $result
        );
    }
}