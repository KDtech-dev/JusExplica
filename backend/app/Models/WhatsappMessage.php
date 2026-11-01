<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class WhatsappMessage extends Model
{
    protected $fillable = [
        'conversation_id',
        'message_id',
        'direction',
        'type',
        'content',
        'media_path',
    ];

    public function conversation(): BelongsTo
    {
        return $this->belongsTo(
            WhatsappConversation::class,
            'conversation_id'
        );
    }
}