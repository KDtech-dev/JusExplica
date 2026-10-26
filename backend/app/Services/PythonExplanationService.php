<?php

namespace App\Services;

use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;

class PythonExplanationService
{
    /**
     * @throws ConnectionException
     */
    public function explain(array $payload): Response
    {
        $baseUrl = rtrim(
            config('services.python_explanation.url'),
            '/'
        );

        return Http::acceptJson()
            ->asJson()
            ->connectTimeout(3)
            ->timeout(20)
            ->post(
                "{$baseUrl}/v1/explanations",
                $payload
            );
    }
}