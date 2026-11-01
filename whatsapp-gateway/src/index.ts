import makeWASocket, {
    DisconnectReason,
    useMultiFileAuthState,
} from '@whiskeysockets/baileys';
import { sendMessageToLaravel } from './services/api.service.js';
import pino from 'pino';
import qrcode from 'qrcode-terminal';

async function connectToWhatsApp(): Promise<void> {
    const { state, saveCreds } = await useMultiFileAuthState(
        'auth_info'
    );

    const socket = makeWASocket({
        auth: state,
        logger: pino({ level: 'silent' }),
        printQRInTerminal: false,
    });

    socket.ev.on('creds.update', saveCreds);

    socket.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log('\nEscaneie o QR Code com seu WhatsApp:\n');
            qrcode.generate(qr, { small: true });
        }

        if (connection === 'open') {
            console.log('WhatsApp conectado com sucesso!');
        }

        if (connection === 'close') {
            const statusCode = (
                lastDisconnect?.error as any
            )?.output?.statusCode;

            const shouldReconnect =
                statusCode !== DisconnectReason.loggedOut;

            console.log('Conexão encerrada.');

            if (shouldReconnect) {
                console.log('Tentando reconectar...');
                await connectToWhatsApp();
            } else {
                console.log(
                    'Sessão encerrada. Será necessário conectar novamente.'
                );
            }
        }
    });

    socket.ev.on('messages.upsert', async ({ messages, type }) => {
        if (type !== 'notify') return;

        for (const message of messages) {
            const remoteJid = message.key.remoteJid;

            if (!remoteJid || message.key.fromMe) continue;

            // Ignora grupos e mensagens de status.
            if (
                remoteJid.endsWith('@g.us') ||
                remoteJid === 'status@broadcast'
            ) {
                continue;
            }

            const content =
                message.message?.conversation ??
                message.message?.extendedTextMessage?.text;

            if (!content) continue;

            console.log('\nNova mensagem recebida:');
            console.log('Remetente:', remoteJid);
            console.log('Mensagem:', content);

            try {
                const reply = await sendMessageToLaravel({
                    message_id: message.key.id ?? '',
                    sender: remoteJid,
                    type: 'text',
                    content,
                    timestamp: new Date(
                        Number(message.messageTimestamp ?? 0) * 1000
                    ).toISOString(),
                });

                if (reply) {
                    await socket.sendMessage(remoteJid, { text: reply });
                    console.log('Resposta enviada:', reply);
                }

                console.log('Resposta enviada:', reply);

            } catch (error) {
                console.error(
                    'Erro ao processar mensagem:',
                    error
                );

                await socket.sendMessage(remoteJid, {
                    text: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.',
                });
            }
        }
    });
}

connectToWhatsApp().catch(console.error);