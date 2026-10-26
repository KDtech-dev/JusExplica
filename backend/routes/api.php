<?php

use App\Http\Controllers\Api\ExplanationController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::post('/explanations', [
    ExplanationController::class,
    'store',
]);