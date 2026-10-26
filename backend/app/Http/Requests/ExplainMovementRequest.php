<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ExplainMovementRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'movement' => [
                'required',
                'array:code,description,date',
            ],

            'movement.code' => [
                'required',
                'string',
                'max:100',
            ],

            'movement.description' => [
                'required',
                'string',
                'max:2000',
            ],

            'movement.date' => [
                'sometimes',
                'nullable',
                'date_format:Y-m-d',
            ],

            'language' => [
                'sometimes',
                'string',
                'min:2',
                'max:10',
            ],
        ];
    }
}