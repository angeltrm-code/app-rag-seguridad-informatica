# Plan de Seguridad Informática Integral

## Resumen Ejecutivo

El presente documento establece el marco de seguridad informática para la organización, definiendo las medidas de protección necesarias, el plan de implementación por fases y los mecanismos de verificación continua.

El plan se estructura en **12 dominios de seguridad** y propone un **roadmap de implementación en cuatro fases** (0–30, 30–90, 90–180 y 180+ días), priorizando las acciones de mayor impacto inmediato.

Las recomendaciones contenidas en este informe se fundamentan exclusivamente en marcos de referencia reconocidos: ENS, NIST CSF v2, CIS Benchmarks, y guías del CCN-CERT e INCIBE. No se ha incluido contenido que no esté respaldado por la documentación de referencia analizada.

**Principales áreas de actuación:**

- Implantación de autenticación multifactor y gestión de identidades
- Bastionado de endpoints y servidores (Windows, macOS, dispositivos móviles)
- Protección del perímetro de red y cifrado de comunicaciones
- Estrategia de copias de seguridad y recuperación ante desastres
- Desarrollo de un plan de respuesta a incidentes y continuidad de negocio
- Programa de concienciación y formación en ciberseguridad

---

## Alcance, Supuestos y Exclusiones

### Alcance

Este plan cubre la totalidad de los dominios de seguridad de la información aplicables a la organización:

| Dominio | Cobertura |
|---------|-----------|
| Gobernanza y gestión de riesgos | Completa |
| Normativa y cumplimiento (ENS, RGPD, NIST) | Completa |
| Identidad y control de acceso | Completa |
| Endpoint y bastionado | Completa |
| Red y perímetro | Completa |
| Correo electrónico y navegadores | Completa |
| Dispositivos móviles | Completa |
| Nube y virtualización | Completa |
| Desarrollo seguro | Completa |
| Respuesta a incidentes y continuidad | Completa |
| Concienciación y formación | Completa |
| Monitorización y amenazas emergentes | Completa |

### Supuestos

- La organización dispone de infraestructura TI operativa con sistemas Windows y/o macOS.
- Existen servicios de correo electrónico corporativo con dominio propio.
- La organización está sujeta al cumplimiento del ENS y/o RGPD.
- Se dispone de recursos internos o externos para la ejecución técnica de las medidas propuestas.

### Exclusiones

- Seguridad de entornos industriales (OT/ICS/SCADA), salvo que se amplíe el alcance.
- Pruebas de penetración y auditoría de seguridad ofensiva (se proponen como fase posterior).
- Arquitectura Zero Trust detallada (se recomienda como evolución futura).
- Implementación de SOC/SIEM (se describe como recomendación, pendiente de dimensionar).

---

## Situación Actual (AS-IS)

La evaluación de la situación actual se realizará en la fase de discovery. A continuación se presenta la estructura que guiará dicha evaluación:

| Dominio | Estado Estimado | Observaciones |
|---------|----------------|---------------|
| Gobernanza | Pendiente de evaluación | Verificar existencia de política de seguridad y roles designados |
| Normativa | Pendiente de evaluación | Determinar categoría ENS y estado de adecuación |
| IAM | Pendiente de evaluación | Verificar estado de MFA y política de contraseñas |
| Endpoint | Pendiente de evaluación | Inventariar SO y estado de bastionado |
| Red | Pendiente de evaluación | Revisar segmentación y reglas de cortafuegos |
| Correo | Pendiente de evaluación | Verificar registros SPF/DKIM/DMARC |
| Móviles | Pendiente de evaluación | Verificar existencia de MDM |
| Nube | Pendiente de evaluación | Identificar proveedores y certificaciones |
| Desarrollo | Pendiente de evaluación | Revisar ciclo de vida y prácticas actuales |
| Incidentes | Pendiente de evaluación | Verificar existencia de plan de respuesta |
| Concienciación | Pendiente de evaluación | Revisar programa formativo actual |
| Monitorización | Pendiente de evaluación | Evaluar capacidades de detección |

Esta tabla se completará tras el taller de discovery inicial con el equipo técnico y la dirección.

---

## Gobernanza y Gestión de Riesgos

### Marco de Gobernanza

Se propone establecer una estructura de gobernanza de ciberseguridad que incluya:

- **Oficina de Seguridad:** establecimiento de una oficina que asista en la implantación de políticas, procedimientos y normativa para la protección de los activos de la organización.
- **Roles y responsabilidades:** designación formal del Responsable de Seguridad, Responsable del Sistema y Responsable de la Información según los requisitos del ENS.
- **Normativa interna:** desarrollo de políticas que definan las directrices de actuación ante circunstancias no contempladas explícitamente.
- **Capacitación:** plan de formación y concienciación continuo para todo el personal.

### Análisis de Riesgos

- Aplicación de la metodología PILAR para el análisis y gestión de riesgos, incluyendo análisis de impacto y continuidad de operaciones.
- Determinación de la superficie de exposición e inventario de activos y servicios.
- Definición de métricas para la evaluación del desempeño de la gestión de seguridad.

### Plan Director de Seguridad

Elaboración de un Plan Director que establezca objetivos, alcance, fases de implementación e indicadores de seguimiento.

---

## Normativa y Cumplimiento

### Esquema Nacional de Seguridad (ENS)

El proceso de adecuación al ENS contempla las siguientes fases:

1. **Identificación** de servicios e información incluidos en el alcance.
2. **Categorización** del sistema según criterios de disponibilidad, integridad, confidencialidad, autenticidad y trazabilidad.
3. **Declaración de Aplicabilidad** con los controles exigidos según la categoría del sistema.
4. **Implementación** de medidas organizativas, operacionales y de protección.
5. **Auditoría y certificación** periódica del cumplimiento.

### RGPD y Protección de Datos

- Realización de evaluaciones de impacto en la protección de datos (EIPD).
- Designación del Delegado de Protección de Datos cuando sea obligatorio.
- Implementación de medidas técnicas y organizativas para garantizar confidencialidad, integridad, disponibilidad y resiliencia.
- Mantenimiento de registros de actividades de tratamiento.

### NIST Cybersecurity Framework v2

Alineación de controles con las seis funciones del NIST CSF v2: Gobernar (GV), Identificar (ID), Proteger (PR), Detectar (DE), Responder (RS) y Recuperar (RC).

---

## Identidad y Control de Acceso

### Autenticación

- **Autenticación multifactor (MFA) obligatoria** en todos los accesos a sistemas críticos. El tipo y método de autenticación deben formar parte del diseño desde el inicio.
- **Tipos soportados:** tokens físicos o digitales, biometría, certificados electrónicos, tarjetas inteligentes.
- **Política de bloqueo:** bloqueo automático de cuentas tras 3 intentos fallidos consecutivos.

### Gestión de Credenciales

- Políticas de complejidad y rotación de contraseñas.
- Prohibición de almacenamiento de credenciales en texto claro.
- Uso de gestores de contraseñas corporativos.

### Principio de Privilegio Mínimo

- Asignación de permisos según la necesidad operativa (need-to-know).
- Revisiones periódicas de permisos y accesos privilegiados.
- Segmentación de roles administrativos.

---

## Endpoint y Bastionado

### Configuración Segura de Endpoints

- Aplicación de baselines de bastionado según el sistema operativo.
- Cifrado de todas las comunicaciones entre endpoints y servicios.
- Control de dispositivos USB, cifrado de disco completo y protección anti-malware.

### Windows

- Aplicación del CIS Benchmark para Windows 11 Enterprise v4.0.0 (1.466 controles documentados).
- Configuración de políticas de grupo (GPO): auditoría, control de cuentas, cifrado BitLocker, Windows Defender, firewall y restricción de software.

### macOS

- Aplicación de las recomendaciones de seguridad del CCN-CERT para macOS.
- Configuración de FileVault, Gatekeeper, firewall integrado y System Integrity Protection.
- Gestión centralizada de actualizaciones.

### Gestión de Configuración

Implementación de un control efectivo de configuración y gestión de software, garantizando que los archivos ejecutables y plantillas compartidas residan en directorios de solo lectura.

---

## Red y Perímetro

### Cortafuegos y Segmentación

- Establecimiento de políticas de red que permitan controlar granularmente las conexiones permitidas.
- Aproximación de lista blanca (whitelisting): habilitación únicamente de las conectividades estrictamente necesarias.
- Segmentación de red por zonas de seguridad (DMZ, LAN interna, gestión).

### Comunicaciones Cifradas (HTTPS/TLS)

- Forzado de HTTPS en todos los servicios web internos y externos.
- Configuración de TLS 1.2 como mínimo (preferiblemente TLS 1.3).
- Gestión centralizada de certificados digitales.

### Protección frente a Denegación de Servicio

- Implementación de medidas anti-DDoS en cortafuegos perimetrales.
- Evaluación del uso de CDN con capacidades de mitigación.

### Redes Inalámbricas

- Uso de WPA3 (o WPA2-Enterprise con RADIUS como mínimo).
- Separación de redes WiFi corporativas, de invitados y de IoT.

---

## Correo Electrónico y Navegadores

### Seguridad del Correo

- **SPF, DKIM y DMARC** en todos los dominios corporativos:
  - SPF: verificación del dominio remitente autorizado.
  - DKIM: firma digital de correos salientes.
  - DMARC: política objetivo `p=reject` para protección contra spoofing.
- Cifrado de comunicaciones sensibles mediante GPG/S-MIME.

### Navegadores Web

- Aplicación de configuraciones de seguridad para Chrome, Firefox y Edge según las guías del CCN-CERT.
- Deshabilitación de plugins innecesarios, forzado de actualizaciones automáticas.
- Políticas de navegación segura y lista blanca de extensiones.

---

## Dispositivos Móviles

### Gestión MDM

- Implementación de una solución de Mobile Device Management (MDM) centralizada.
- Definición de perfiles de configuración con valores recomendados por plataforma.
- Evaluación de funcionalidades MDM según las plataformas en uso.

### Políticas por Plataforma

- **Android:** aplicación de las configuraciones de seguridad documentadas (162+ controles).
- **iOS/iPad:** empleo seguro según las guías del CCN-STIC para iOS 18 y servicios Apple.
- **BYOD:** políticas de separación de datos corporativos y personales.

### Seguridad Nativa

- Aprovechamiento de capacidades integradas: Secure Enclave, cifrado en reposo, sandboxing de aplicaciones.
- Restricciones de instalación de aplicaciones y control de funcionalidades.

---

## Nube y Virtualización

### Protección del Dato en la Nube

- Las medidas de seguridad deben implementarse de forma preventiva, antes de que se produzca un incidente.
- Firma de Acuerdos de Nivel de Servicio (ANS) que garanticen disponibilidad, integridad, confidencialidad y trazabilidad.
- Verificación de certificaciones del proveedor cloud cuando se requiera cumplimiento con el ENS.

### Virtualización

- Aplicación de buenas prácticas de seguridad en entornos virtualizados.
- Aislamiento de hipervisores y redes de gestión.
- Cifrado de comunicaciones entre nodos virtuales.

### Contenedores y Orquestación

- Aplicación de las recomendaciones de seguridad para Kubernetes del CCN-CERT.
- Configuración de RBAC, network policies y pod security standards.
- Escaneo de imágenes de contenedores previo al despliegue.

### Copias de Seguridad

- Implementación de la regla 3-2-1: 3 copias, 2 medios distintos, 1 fuera de las instalaciones.
- Verificación periódica de la integridad y restaurabilidad de las copias.
- Dimensionamiento del ancho de banda necesario para copias en la nube.

---

## Desarrollo Seguro

### Principios

- Protección de datos mediante mecanismos de autorización y segmentación entre entornos.
- Uso exclusivo de medios externos autorizados.
- Borrado seguro obligatorio de archivos con información sensible.

### Controles por Fase del Ciclo de Vida

| Fase | Controles Clave |
|------|----------------|
| Diseño | Modelado de amenazas, requisitos de seguridad, MFA, protección de datos sensibles |
| Desarrollo | Revisión de código, SAST, gestión de dependencias, secrets management |
| Testing | DAST, pruebas de penetración, fuzzing |
| Despliegue | Bastionado de servidores, CI/CD seguro, configuración segura |
| Operación | Monitorización, parcheado, respuesta a incidentes |

### Seguridad en CMS y Bases de Datos

- **CMS (Drupal):** aplicación de las 78 recomendaciones de la guía CCN-STIC.
- **Bases de datos:** bastionado de BBDD (DB2 y general), restricción de accesos administrativos, cifrado de datos sensibles.

---

## Respuesta a Incidentes y Continuidad

### Gestión de Cibercrisis

- Establecimiento de un procedimiento formal de gestión de cibercrisis con roles, canales de comunicación y escalado definidos.
- Realización de ejercicios periódicos de simulación.
- Preparación organizativa previa: la capacidad de respuesta debe construirse antes de que se produzca un incidente.

### Ransomware

| Fase | Medidas |
|------|---------|
| Prevención | Segmentación de red, copias de seguridad offline, MFA, parcheo continuo |
| Detección | Monitorización de comportamientos anómalos, EDR/XDR |
| Respuesta | Aislamiento de equipos afectados, preservación de evidencias, comunicación de crisis |
| Recuperación | Restauración desde copias limpias, verificación de integridad previa a la reconexión |

### Continuidad de Negocio

- Elaboración de BCP/DRP con RTOs y RPOs definidos para cada servicio crítico.
- Uso de la herramienta PILAR para el análisis de impacto y continuidad de operaciones.
- Pruebas de recuperación con periodicidad mínima anual.

### Prevención de Fuga de Información

- Implementación de herramientas DLP (Data Loss Prevention).
- Clasificación de la información por niveles de sensibilidad.
- Medidas preventivas implementadas antes de la ocurrencia de incidentes.

---

## Concienciación, IoT y Amenazas Emergentes

### Formación y Concienciación

- Programa de concienciación continuo para todos los niveles de la organización.
- Simulaciones de phishing periódicas con seguimiento de resultados.
- Formación específica por perfil: técnico, directivo y usuario general.

### Internet de las Cosas (IoT)

- Inventario completo de dispositivos IoT conectados a la red.
- Segmentación de la red IoT respecto a la red corporativa.
- Políticas de actualización de firmware y cambio de credenciales por defecto.

### Amenazas Emergentes

- **Cryptojacking:** monitorización de consumo anómalo de CPU/GPU, bloqueo de scripts de minería.
- **Inteligencia artificial en ciberseguridad:** evaluación de capacidades de detección basada en machine learning.
- **Desinformación:** protocolos de respuesta ante campañas que puedan afectar a la organización.

---

## Teletrabajo

### Recomendaciones

- Conexiones VPN con autenticación fuerte (MFA).
- Políticas de seguridad específicas para equipos remotos.
- Cifrado completo de disco en portátiles corporativos.
- Gestión de sesiones remotas con timeout y bloqueo automático.
- Separación de entornos personales y corporativos en equipos de teletrabajo.

---

## Roadmap de Implementación por Fases

### Fase 0 — Higiene Base (0–30 días)

| Acción | Dominio | Prioridad |
|--------|---------|-----------|
| Activar MFA en todos los accesos críticos | IAM | CRÍTICA |
| Implementar copias de seguridad 3-2-1 | Backup | CRÍTICA |
| Inventario de activos y servicios | Gobernanza | CRÍTICA |
| Aplicar SPF+DKIM+DMARC en dominios de correo | Correo | CRÍTICA |
| Segmentar red WiFi (corporativa vs. invitados) | Red | ALTA |
| Bastionado básico de endpoints (antivirus, firewall, cifrado) | Endpoint | ALTA |
| Programa de concienciación básico | Personas | ALTA |

### Fase 1 — Bastionado Sistemático (30–90 días)

| Acción | Dominio | Prioridad |
|--------|---------|-----------|
| Aplicar CIS Benchmark en Windows | Endpoint | ALTA |
| Configurar HTTPS/TLS en todos los servicios | Red | ALTA |
| Implementar MDM para dispositivos móviles | Móviles | ALTA |
| Bastionado de navegadores (Chrome/Firefox/Edge) | Navegadores | MEDIA |
| Configurar whitelisting de red en cortafuegos | Red | ALTA |
| Bastionado de bases de datos | AppSec | MEDIA |
| Configurar seguridad en entornos cloud/virtual | Nube | MEDIA |

### Fase 2 — Gobernanza y Normativa (90–180 días)

| Acción | Dominio | Prioridad |
|--------|---------|-----------|
| Elaborar Plan Director de Seguridad | Gobernanza | ALTA |
| Análisis de riesgos con PILAR | Riesgos | ALTA |
| Declaración de Aplicabilidad ENS | Normativa | ALTA |
| Política de desarrollo seguro (SSDLC) | AppSec | MEDIA |
| Procedimientos de respuesta a incidentes | IR | ALTA |
| Plan de continuidad de negocio (BCP/DRP) | Continuidad | MEDIA |
| Adecuación RGPD | Legal | MEDIA |

### Fase 3 — Mejora Continua (180+ días)

| Acción | Dominio | Prioridad |
|--------|---------|-----------|
| Ejercicios de cibercrisis y simulacros | IR | MEDIA |
| Pruebas de penetración periódicas | AppSec | MEDIA |
| Métricas de seguridad y cuadros de mando | Gobernanza | MEDIA |
| Integración de IA para detección de amenazas | Monitorización | NORMAL |
| Revisión y actualización anual del plan | Gobernanza | MEDIA |

---

## Matriz de Riesgos

A continuación se presenta una valoración inicial de los principales riesgos identificados, basada en los dominios evaluados. Esta matriz se refinará tras la fase de discovery.

| Riesgo | Probabilidad | Impacto | Nivel | Mitigación Propuesta |
|--------|-------------|---------|-------|---------------------|
| Acceso no autorizado por ausencia de MFA | Alta | Crítico | CRÍTICA | Implantación inmediata de MFA en sistemas críticos |
| Pérdida de datos por falta de copias de seguridad | Media | Crítico | CRÍTICA | Estrategia 3-2-1 con verificación periódica |
| Ransomware por endpoint no bastionado | Alta | Crítico | CRÍTICA | CIS Benchmark + EDR + segmentación de red |
| Suplantación de identidad por correo (phishing) | Alta | Alto | ALTA | SPF+DKIM+DMARC + programa de concienciación |
| Fuga de información por dispositivo móvil no gestionado | Media | Alto | ALTA | MDM + políticas BYOD + cifrado |
| Exposición de servicios internos sin cifrar | Media | Alto | ALTA | Forzado de HTTPS/TLS en todos los servicios |
| Incumplimiento normativo (ENS/RGPD) | Media | Alto | ALTA | Plan de adecuación con calendario definido |
| Vulnerabilidades en aplicaciones web | Media | Medio | MEDIA | SSDLC + SAST/DAST + bastionado CMS |
| Acceso a la red por dispositivos IoT inseguros | Baja | Medio | MEDIA | Segmentación de red IoT + inventario |
| Interrupción de negocio sin plan de recuperación | Baja | Crítico | ALTA | BCP/DRP con pruebas anuales |

---

## Matriz RACI

Asignación genérica de responsabilidades por dominio de actuación. Se ajustará a la estructura organizativa real tras la fase de discovery.

| Actividad | Responsable (R) | Aprobador (A) | Consultado (C) | Informado (I) |
|-----------|-----------------|---------------|-----------------|---------------|
| Gobernanza y políticas | CISO / Resp. Seguridad | Dirección General | Legal, IT | Todos |
| Análisis de riesgos | Resp. Seguridad | CISO | Áreas de negocio | Dirección |
| Bastionado de endpoints | Equipo Sistemas | Resp. Seguridad | Soporte IT | CISO |
| Gestión de red y perímetro | Equipo Redes | Resp. Seguridad | Arquitectura IT | CISO |
| Seguridad del correo | Equipo Sistemas | Resp. Seguridad | Comunicación | Usuarios |
| Gestión de móviles (MDM) | Equipo Sistemas | Resp. Seguridad | RRHH | Usuarios |
| Seguridad en la nube | Equipo Cloud | Resp. Seguridad | Proveedores | CISO |
| Desarrollo seguro | Equipo Desarrollo | Resp. Seguridad | QA | CISO |
| Respuesta a incidentes | CSIRT / Resp. Seguridad | Dirección | Legal, Comunicación | Todos |
| Concienciación y formación | RRHH / Resp. Seguridad | Dirección | Comunicación | Todos |
| Cumplimiento normativo | Legal / DPO | Dirección General | Resp. Seguridad | Auditoría |
| Copias de seguridad | Equipo Sistemas | Resp. Seguridad | Áreas críticas | CISO |

---

## Checklist de Implementación y Evidencias

| Control | Entregable | Evidencia requerida al cliente |
|---------|-----------|-------------------------------|
| MFA activo | Configuración de MFA en sistemas críticos | Captura de configuración, informe de cobertura |
| Copias de seguridad | Estrategia 3-2-1 implementada | Logs de ejecución + prueba de restauración |
| Antivirus/EDR | Protección desplegada en endpoints | Dashboard de estado de protección |
| Cortafuegos | Reglas de segmentación aplicadas | Reglas exportadas + changelog |
| SPF/DKIM/DMARC | Registros DNS configurados | Registros DNS + informes DMARC |
| Bastionado Windows | CIS Benchmark aplicado | Resultado de escaneo CIS-CAT o equivalente |
| MDM | Dispositivos gestionados | Lista de dispositivos + políticas activas |
| Cifrado de disco | BitLocker/FileVault habilitado | Estado de cifrado en inventario |
| Formación | Programa de concienciación ejecutado | Registro de asistencia + resultados phishing |
| Incidentes | Plan de respuesta documentado | Procedimiento + registro de incidentes |
| Actualizaciones | Parcheado gestionado | Informe de vulnerabilidades pendientes |
| Privilegios | Revisión de accesos completada | Listado de usuarios con permisos administrativos |

---

## Próximos Pasos

### Fase Inmediata (próximas 2 semanas)

1. **Taller de Discovery:** sesión conjunta con el equipo técnico y la dirección para:
   - Completar la evaluación AS-IS de la tabla de situación actual.
   - Identificar sistemas críticos y prioridades específicas.
   - Validar el roadmap propuesto y ajustar plazos.

2. **Recolección de evidencias inicial:** el equipo facilitará:
   - Inventario de activos y servicios TI.
   - Configuración actual de correo (registros DNS).
   - Estado de los endpoints (SO, antivirus, cifrado).
   - Diagrama de red (si existe).

3. **Validación del plan:** revisión conjunta del presente documento con los responsables para confirmar prioridades y asignación de recursos.

### Calendario Propuesto

| Hito | Plazo |
|------|-------|
| Taller de discovery | Semana 1 |
| Entrega de evaluación AS-IS completada | Semana 2 |
| Inicio de Fase 0 (higiene base) | Semana 3 |
| Revisión de progreso Fase 0 | Semana 6 |
| Inicio de Fase 1 (bastionado) | Semana 7 |
| Revisión de progreso Fase 1 | Semana 13 |
| Inicio de Fase 2 (gobernanza) | Semana 14 |

---

## Referencias Consultadas

Las recomendaciones de este plan se fundamentan en las siguientes familias de marcos, estándares y guías de referencia:

| Familia | Ámbito |
|---------|--------|
| CCN-CERT (Buenas Prácticas) | Guías de bastionado, correo, navegadores, teletrabajo, cibercrisis, ransomware, desarrollo seguro, IoT, IA, bases de datos, virtualización, nube |
| CCN-STIC | Guías de seguridad de dispositivos móviles, Apple, Drupal, PILAR, endpoint, etiquetas de seguridad |
| INCIBE | Guías empresariales de ciberseguridad, gestión de riesgos, ransomware, copias de seguridad, WiFi, IoT, teletrabajo, fuga de información, RGPD, plan director |
| NIST | Cybersecurity Framework v2 (CSF) |
| CIS | Center for Internet Security — Benchmark Windows 11 Enterprise v4.0.0 |
| Apple | Apple Platform Security Guide |

---

## Cobertura y Limitaciones

### Cobertura del análisis

El corpus documental analizado (70 documentos) proporciona cobertura amplia en:
- Gobernanza y normativa (ENS, NIST, RGPD)
- Endpoint (Windows, macOS, dispositivos móviles)
- Red y perímetro (HTTPS, DDoS, WiFi)
- Correo electrónico (DMARC, SPF, DKIM)
- Respuesta a incidentes y ransomware
- Nube y virtualización

### Áreas recomendadas para ampliación futura

- SIEM/SOC: guías específicas de monitorización y detección.
- Zero Trust: documentación de arquitecturas Zero Trust.
- OT/ICS: si existen entornos industriales, guías ICS/SCADA.
- Pentesting: metodologías PTES/OSSTMM para test de intrusión.
