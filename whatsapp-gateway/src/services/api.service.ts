interface LaravelResponse {
    success: boolean;
    message: string;
    data?: {
        reply: string | null;
        duplicate: boolean;
    };
}

const API_URL = process.env.LARAVEL_API_URL;

export async function sendMessageToLaravel(payload: {
    message_id: string;
    sender: string;
    type: 'text';
    content: string;
    timestamp: string;
}): Promise<string | null> {
    if (!API_URL) {
        throw new Error('LARAVEL_API_URL não configurada.');
    }

    const response = await fetch(
        `${API_URL}/internal/whatsapp/messages`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(`Laravel retornou HTTP ${response.status}`);
    }

    const result = await response.json() as LaravelResponse;

    if (!result.success || !result.data) {
        throw new Error('Resposta inválida do Laravel.');
    }

    if (result.data.duplicate) {
        return null;
    }

    if (!result.data.reply) {
        throw new Error('Laravel não retornou uma resposta.');
    }

    return result.data.reply;
}