<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\ExplainMovementRequest;
use App\Services\PythonExplanationService;
use App\Services\ResponseService;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\JsonResponse;

class ExplanationController extends Controller
{
    public function store(
        ExplainMovementRequest $request,
        PythonExplanationService $pythonService,
        ResponseService $responseService
    ): JsonResponse {
        $payload = $request->validated();

        $payload['language'] ??= 'pt-BR';

        try {
            $response = $pythonService->explain($payload);
        } catch (ConnectionException $exception) {
            report($exception);

            return $responseService->error(
                'O serviço de explicações está indisponível.',
                503
            );
        }

        if (! $response->successful()) {
            report(
                'O serviço Python retornou HTTP ' . $response->status()
            );

            return $responseService->error(
                'Não foi possível gerar a explicação.',
                502
            );
        }

        return $responseService->success(
            'Explicação gerada com sucesso.',
            $response->json('data')
        );
    }
}