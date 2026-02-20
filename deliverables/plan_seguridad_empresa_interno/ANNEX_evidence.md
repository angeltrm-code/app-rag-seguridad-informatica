# Anexo de Evidencia y Trazabilidad

## Propósito

Este anexo documenta las fuentes consultadas para la elaboración del Plan de Seguridad,
proporcionando trazabilidad completa para fines de auditoría interna.

## Corpus Documental

- **Total de documentos analizados:** 70
- **Total de fragmentos indexados:** 8.580
- **Fragmentos utilizados como evidencia:** 249
- **Documentos consultados directamente:** 59

## Fuentes por Dominio

### Gobernanza y Gestión de Riesgos
- `00-gobernanza_marco_ciberseguridad.md` — pp. 1 y ss.
- `16-principios_recomendaciones_basicas.md` — pp. 4–45
- `05-ens_medidas_implantacion.md` — pp. 10 y ss.
- `15-plan_director_seguridad.md` — pp. 1 y ss.
- `09-pilar_analisis_gestion_riesgos.md` — pp. 1 y ss.

### Normativa y Cumplimiento
- `00-gobernanza_marco_ciberseguridad.md` — pp. 21 y ss.
- `06-ens_declaracion_aplicabilidad.md` — pp. 1 y ss.
- `07-nist_csf_v2.md` — pp. 1 y ss.
- `08-cumplimiento_legal_incibe.md` — pp. 1 y ss.
- `17-rgpd_competitividad_2024.md` — pp. 1 y ss.

### Identidad y Control de Acceso
- `62-desarrollo_seguro.md` — pp. 76 y ss.
- `01-glosario_ccn.md` — pp. 126 y ss.
- `27-identidad_digital_ciberseguridad.md` — pp. 1 y ss.
- `16-principios_recomendaciones_basicas.md` — pp. 4 y ss.

### Endpoint y Bastionado
- `40-endpoint_seguro.md` — pp. 1–55
- `41-endpoint_seguro_anexo.md` — pp. 1–19
- `42-windows11_cis_benchmark.md` — pp. 1–1.466
- `43-macos_seguridad.md` — pp. 1–49
- `16-principios_recomendaciones_basicas.md` — pp. 45 y ss.

### Red y Perímetro
- `22-ransomware_incidentes_ccn.md` — pp. 3 y ss.
- `33-proteccion_dos_cortafuegos.md` — pp. 1–21
- `32-https_seguridad.md` — pp. 1–106
- `34-cdn_recomendaciones.md` — pp. 1–37
- `35-seguridad_redes_wifi.md` — pp. 1–30

### Correo Electrónico y Navegadores
- `31-correo_dmarc.md` — pp. 1–50
- `30-correo_electronico_seguridad.md` — pp. 1–48
- `38-chrome_seguridad.md` — pp. 1–32
- `37-firefox_seguridad.md` — pp. 1–54
- `39-edge_seguridad.md` — pp. 1–40
- `36-navegadores_web_seguridad.md` — pp. 1–48

### Dispositivos Móviles
- `48-mdm_gestion_dispositivos.md` — pp. 9–97
- `44-dispositivos_moviles_seguridad.md` — pp. 1–48
- `45-android_seguridad.md` — pp. 1–162
- `49-ios18_empleo_seguro.md` — pp. 1–38
- `50-apple_platform_security.md` — pp. 1–262
- `51-apple_servicios_seguridad.md` — pp. 1–123

### Nube y Virtualización
- `53-nube_proteccion_dato_soberania.md` — pp. 4–71
- `52-virtualizacion_buenas_practicas.md` — pp. 1–63
- `68-kubernetes_seguridad.md` — pp. 1–43
- `57-copias_seguridad.md` — pp. 1–32
- `55-almacenamiento_nube.md` — pp. 1–7

### Desarrollo Seguro
- `62-desarrollo_seguro.md` — pp. 1–96
- `63-drupal_seguridad.md` — pp. 1–78
- `64-bbdd_db2_seguridad.md` — pp. 1–35
- `65-bbdd_seguridad_general.md` — pp. 1–34

### Respuesta a Incidentes y Continuidad
- `18-gestion_cibercrisis.md` — pp. 1–48
- `19-cibercrisis_entidades_locales.md` — pp. 1–92
- `20-gestion_crisis_incibe.md` — pp. 1–51
- `21-ransomware_ccn.md` — pp. 1–46
- `22-ransomware_incidentes_ccn.md` — pp. 1–37
- `23-ransomware_incibe.md` — pp. 1–34
- `24-fuga_informacion.md` — pp. 1–20
- `11-pilar_impacto_continuidad.md` — pp. 1 y ss.

### Concienciación, IoT y Amenazas Emergentes
- `69-concienciacion_formacion.md` — pp. 1–7
- `58-iot_seguridad.md` — pp. 1–28
- `59-iot_ccn.md` — pp. 1–49
- `61-cryptojacking.md` — pp. 1–32
- `28-inteligencia_artificial_ccn.md` — pp. 1–107
- `26-desinformacion_ciberespacio.md` — pp. 1–51
- `60-redes_sociales.md` — pp. 1–62

### Teletrabajo
- `66-teletrabajo_ccn.md` — pp. 1–84
- `67-teletrabajo_incibe.md` — pp. 1–44

## Método de Recuperación

Las evidencias se extrajeron mediante búsqueda híbrida (FAISS vectorial + BM25 léxico) con fusión RRF sobre un índice de 8.580 chunks generados por el pipeline RAG del proyecto.
