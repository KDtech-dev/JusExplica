"use client";

import { ArrowUp, AudioLines, Scale } from "lucide-react";
import "./globals.css";

export default function Home() {
  return (
    <main className="pagina">
      <header className="cabecalho">
        <a href="/" className="logo">
          <span className="logo-icone">
            <Scale />
          </span>
          <span>JusExplica</span>
        </a>

        <span className="cabecalho-texto">
          Informação jurídica para todos
        </span>
      </header>

      <section className="hero">
        <h1>
          A Justiça fala
          <br />
          <span>a sua língua.</span>
        </h1>
      </section>

      <section
        className="area-chat"
        aria-label="Chat JusExplica"
      >
        <form
          className="chat-compositor"
          onSubmit={(event) => event.preventDefault()}
        >
          <button
            className="botao-mais"
            type="button"
            aria-label="Adicionar"
          >
            +
          </button>

          <input
            className="chat-input"
            type="text"
            name="mensagem"
            placeholder="Digite sua dúvida sobre seus direitos..."
            aria-label="Digite sua mensagem"
          />

          <button
            className="botao-enviar"
            type="button"
            aria-label="Enviar mensagem"
          >
            <ArrowUp aria-hidden="true" />
          </button>

          <button
            className="botao-audio"
            type="button"
            aria-label="Enviar áudio"
          >
            <AudioLines aria-hidden="true" />
          </button>
        </form>
      </section>
    </main>
  );
}