# Prompt: Modo Consulta (Q&A / RAG Answer)

## Instrucciones

Responde a la consulta del usuario utilizando **exclusivamente** el contexto proporcionado a continuación. Sigue estas reglas:

1. **Analiza** todos los fragmentos de contexto proporcionados.
2. **Identifica** la información relevante para la consulta.
3. **Sintetiza** una respuesta completa y accionable.
4. **Cita** cada afirmación con su fuente.

## Contexto recuperado

{context}

## Consulta del usuario

{query}

## Formato de respuesta

### Respuesta

[Tu respuesta aquí, estructurada con:]
- **Qué**: descripción clara de la recomendación o información
- **Por qué**: justificación basada en el contexto recuperado
- **Cómo**: pasos concretos de implementación (si aplica)
- **Riesgos/limitaciones**: advertencias relevantes

### Fuentes

* `{source_file}` — `{section_path}` — páginas `{page_start}-{page_end}`

---

> Si no encuentras información suficiente en el contexto, responde:
> **"No encuentro evidencia suficiente en la documentación indexada para responder a esta consulta. Sería necesario disponer de documentación sobre: [tema específico]."**
