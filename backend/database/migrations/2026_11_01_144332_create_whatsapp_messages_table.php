<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
      Schema::create('whatsapp_messages', function (Blueprint $table) {
    $table->id();

    $table->foreignId('conversation_id')
        ->constrained('whatsapp_conversations')
        ->cascadeOnDelete();

    $table->string('message_id', 255);
    $table->string('direction', 20);
    $table->string('type', 20);
    $table->longText('content')->nullable();
    $table->string('media_path')->nullable();

    $table->timestamps();

    $table->unique(
        ['conversation_id', 'message_id'],
        'whatsapp_messages_conversation_message_unique'
    );
});
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('whatsapp_messages');
    }
};
