<?php

namespace App\Http\Requests\Whatsapp;

use Illuminate\Foundation\Http\FormRequest;

class ReceiveMessageRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'message_id' => ['required', 'string', 'max:255'],
            'sender' => ['required', 'string', 'max:50'],
            'type' => ['required', 'in:text,audio'],
            'content' => ['required', 'string', 'max:5000'],
            'timestamp' => ['nullable', 'date'],
        ];
    }
}