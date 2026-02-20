# Plan de Seguridad Informática Empresarial
**Nivel:** Estratégico y Operativo (vCISO)
**Audiencia:** Ejecutiva (Client-Facing)

## 0. Portada y Control de Versión
* **Cliente / Proyecto:** [Nombre de Empresa] - Transformación en Ciberseguridad GRC
* **Fecha:** Febrero 2026
* **Versión:** 2.0 (Tri-SO & RGPD)
* **Estado:** FINAL
* **Autor:** Equipo vCISO y Arquitectura de Seguridad

---

## 1. Resumen Ejecutivo
Este plan estratégico establece los cimientos defensivos y normativos para [Nombre de Empresa], fundamentado en los controles de ENS, NIST CSF v2, y la legislación de protección de datos (RGPD/LOPDGDD).

* **Top Riesgos Identificados:** 1) Infección por Ransomware, 2) Fuga de Información PII, 3) Movimiento lateral desde endpoints comprometidos, 4) Accesos cloud no autorizados, 5) Pérdida de continuidad de negocio.
* **Quick Wins (0–30 días):** 
  * Despliegue de MFA forzado para accesos VPN y Cloud.
  * Cifrado de discos en el 100% del parque (BitLocker/FileVault/LUKS).
  * Despliegue de EDR base en endpoints.
  * Actualización del Registro de Actividades de Tratamiento (ROPA).

---

## 2. Alcance y Supuestos
* **Entornos Cubiertos:** Endpoints y Servidores. Operación On-Premise y Cloud Híbrido (AWS/Azure).
* **Plataformas Homologadas (Tri-SO):** 
  * Windows 11 / Windows Server 2022 o superior.
  * macOS (Apple Silicon e Intel soportado).
  * Linux (RHEL 9, Debian 12, SLES).
* **Supuestos:** Apoyo explícito de Dirección General mediante un Comité de Seguridad. Centralización de identidades en Active Directory / Entra ID.
* **Exclusiones:** Sistemas industriales (OT) y sistemas operativos obsoletos o sin soporte del fabricante; estos se segregarán en redes aisladas (air-gapped) o micro-segmentadas.

---

## 3. Metodología
Las recomendaciones derivan exclusivamente de las siguientes referencias normativas (Corpus Documental Cerrado SSoT):
* **Gobernanza:** Esquema Nacional de Seguridad (ENS).
* **Framework Arquitectura:** NIST CSF v2.
* **Privacidad (GRC):** Guías AEPD y EDPB.
* **Hardening Técnico:** CIS Benchmarks, Guías Apple y Red Hat/SUSE.

---

## 4. Inventario Mínimo Requerido
La gestión de activos es el núcleo fundacional. "No se puede proteger lo que no se conoce" (Control op.act.1).
* **Activos:** Hardware (laptops, servers, móviles) y Software (licencias, SaaS).
* **Identidades:** Empleados, contractors, identidades de servicio (M2M).
* **Datos:** Clasificación de la información corporativa.
* **Procedimiento:** Integración de herramientas de MDM (Intune/Jamf/Apple Business Manager) con herramienta ITSM (CMDB).
* **Evidencias Generadas:** Reporte de cobertura del MDM/CMDB mensual.

---

## 5. Matriz de Riesgos + Risk Register

| ID | Activo/Dato | Escenario | Amenaza | Prob | Impacto | Riesgo | Controles existentes | Recomendación | Riesgo residual | Owner |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Servidores Core | Cifrado masivo de datos e indisponibilidad | Ransomware / Cibercrimen | Alta | Crítico | **Crítico** | Antivirus legacy | EDR avanzado, inmutabilidad de backups intra-red | Medio | SecOps |
| R02 | BBDD y Repositorios | Exfiltración de PII de clientes | Insider / Exfiltración | Media | Crítico | **Alto** | Permisos laxos NTFS/S3 | MFA, RBAC, Cifrado at-rest, DLP | Bajo | IT |
| R03 | Todos los Endpoints | Infección por malware transversal | Phishing / Web surfing | Alta | Alto | **Alto** | Sin filtrado perimetral | Filtro DNS, EDR, Hardening Tri-SO (CIS) | Bajo | IT |
| R04 | Cuentas Privilegiadas Cloud | Compromiso de panel de control cloud | Credenciales débiles expuestas | Alta | Crítico | **Crítico** | Autenticación simple | MFA universal, PAM para administradores (JIT) | Bajo | Arquitect. |
| R05 | Servidores Linux / DMZ | Explotación de RCE por vulnerabilidad pública | Parcheo deficiente | Media | Alto | **Alto** | Parcheo reactivo anual | Gestor de config central (Ansible) + escaneo SCAP | Bajo | IT |
| R06 | Endpoints macOS / Portátiles | Extravío de dispositivo local | Robo físico | Alta | Alto | **Alto** | Claves simples, sin cifrado | FileVault forzado, MDM con remote-wipe | Bajo | IT |
| R07 | Entorno Windows | Elevación de privilegios locales | Movimiento lateral | Alta | Alto | **Alto** | Usuarios son Admin Locales | Retirar Admin Local, LAPS, AppLocker base | Bajo | IT / SecOps |
| R08 | Datos Personales (RH) | Incumplimiento sanciones RGPD | Brecha no notificada (72h) | Baja | Crítico | **Alto** | Sin proceso de RI | Establecer playbooks IR, contacto directo DPO | Bajo | DPO / IR |

---

## 6. Roadmap Ejecutable

| Tarea | Prioridad | Dependencias | Owner | Entregable | Evidencia |
|---|---|---|---|---|---|
| **Fase 1: 0–30 Días (Quick Wins)** | | | | | |
| T01. MFA Universal (VPN/O365) | CRÍTICA | Ninguna | SecOps | Portal SSO protegido | Logs Auth SSO |
| T02. FDE (Cifrado de Discos) Tri-SO | CRÍTICA | Nivel de SO | IT | 100% de PCs cifrados | Reporte MDM Compliance |
| T03. Aprobación Políticas & ROPA | ALTA | Análisis previo | DPO | Políticas V1.0, ROPA V1.0 | Firmas dirección |
| **Fase 2: 30–90 Días (Hardening)** | | | | | |
| T04. Despliegue Agente EDR global | ALTA | Licenciamiento | SecOps | Endpoints monitorizados | Dashboard de EDR >95% |
| T05. Aplicación GPO/Profiles (CIS) | ALTA | Piloto IT | IT | Golden Images seguras | Reportes SCAP/CIS-CAT |
| T06. Segmentación Perimetral/VLAN | MEDIA | Topología Red | Redes | VLANs Usuarios vs Sec | Configs Firewall / ACLs |
| **Fase 3: 90–180 Días (Resiliencia)** | | | | | |
| T07. Plan Continuidad y Pruebas (BIA)| ALTA | Arq. Backups | Riesgos | Doc. BIA y DRP | Alta de Restore exitoso |
| T08. Tabletop Respuesta Incidentes | MEDIA | Playbooks IR | SecOps | Informe Lessons Learned | Resumen ejercicios IR |

---

## 7. Arquitectura Objetivo (Alto Nivel)
La arquitectura objetivo implementa defensa en profundidad:
1. **Identidad (El nuevo perímetro):** SSO y MFA para todos los sistemas (Zero Trust fundamentals).
2. **Endpoints:** Terminales inmutables y gestionados por MDM (Jamf, Intune, Workspace ONE).
3. **Red:** Segmentación estricta separando estaciones de trabajo, servidores (DMZ vs Backend) y gestión.
4. **Cloud:** Uso de Landing Zones seguras, cifrado de repositorios S3/Blob, y evaluación de CSPM continuo.
5. **Backups:** Arquitectura 3-2-1, almacenamiento offline o inmutable, y cifrado out-of-band.

---

## 8. Dominios de Seguridad (D1 - D12)

### D1. Gobierno, Políticas, Roles y Formación
* **Riesgo:** El desconocimiento de la normatividad interna causa exposición.
* **Recomendaciones:**
  * Conformar un **Comité de Ciberseguridad** (Dirección, CISO, Legal, IT) con reuniones trimestrales. (CRÍTICA)
  * Capacitación obligatoria trianual en Anti-Phishing y Privacidad. (ALTA)
* **Implementación:** 1. Redactar borrador de Política General. 2. Firmar por gerencia. 3. Lanzar plataforma LMS.
* **Evidencia:** Actas del comité, certificados de superación de cursos. Frecuencia: Anual.

### D2. Gestión de Activos y Clasificación de Datos
* **Riesgo:** Shadow IT y exposición de PII sin control de acceso.
* **Recomendaciones:**
  * Implementar taxonomía de etiquetas (Ej. *Público, Uso Interno, Confidencial*) en la suite ofimática. (CRÍTICA)
* **Implementación:** Definición en comité → Configuración DLP/AIP → Capacitación.
* **Evidencia:** Repositorio en el MDM/CMDB, reglas DLP activas mapeando las etiquetas confidenciales.

### D3. Identidad y Acceso (IAM)
* **Riesgo:** Credenciales expuestas llevan a compromiso total de dominio.
* **Recomendaciones:**
  * **MFA obligatorio** para todos los accesos externos, VPN y cuentas con privilegios administrativos. (CRÍTICA)
  * **Mínimo Privilegio (RBAC):** Eliminar cuentas genéricas compartidas y usar Privileged Access Management (PAM). (ALTA)
* **Implementación:** Activar Conditional Access Policies en IdP → Auditar cuentas huérfanas mensualmente.
* **Evidencia:** Exportación del IdP mostrando MFA _Enforced_ en un 100% de VPN/Admins.

### D4. Endpoints y Hardening (Tri-SO)
* **Riesgo:** Infección por malware y movimiento lateral entre sistemas operativos.
* **Recomendaciones:**
  * **Hardening Base:** Aplicar perfiles CIS Benchmarks Nivel 1. (ALTA)
  * **Cifrado de Disco Completo (FDE)**. (CRÍTICA)
* **Implementación:** Pilot testing de GPOs/Perfiles MDM → Despliegue masivo → Monitoreo vía SCAP.
* **Evidencias (Control Tri-SO):**

| Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
|---|---|---|---|---|
| **Cifrado (FDE)** | `manage-bde -status` o logs Intune | `fdesetup status` habilitado | Volumen cifrado LUKS activo (`lsblk`) | Quincenal |
| **EDR / AV** | Security Center: Defender Running | Agente EDR activo via MDM System Extension | Servicio local EDR `systemctl status <edr>` | Continuo |
| **Hardening SO** | Reporte CIS / GPO Compliance report | Exportación perfiles `.mobileconfig` MDM | Scaneos OpenSCAP pass rate | Trimestral |
| **Control Periférico**| Políticas USB deshabilitado | Restricción de Media via MDM Payload | Reglas `udev` de bloqueo de almacenamiento | Semestral |

### D5. Red y Perímetro
* **Riesgo:** Acceso irrestricto de atacantes a redes core mediante pivoting.
* **Recomendaciones:**
  * **Segmentación Lógica:** Redes separadas para Visitas, Empleados, IoT, y Servidores mediante NGFW. (CRÍTICA)
  * **Cifrado In-Transit:** Forzar WPA3 o WPA2-Enterprise para Wi-Fi, terminación TLS 1.2+ en webservers. (ALTA)
* **Implementación:** Revisión de arquitectura de red → Ajuste de VLANs → Habilitar ACLs Default-Deny.
* **Evidencias (Control Tri-SO):**

| Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
|---|---|---|---|---|
| **Firewall Host** | `Get-NetFirewallProfile` (Activo) | Perfil local `socketfilterfw` activo | `firewalld` o `ufw` enabled | Mensual |
| **Acceso Red (NAC)**| Certificados EAP-TLS en MMC | Payload Network MDM de tipo TLS | Config de `wpa_supplicant` / cert local | Anual |

### D6. Vulnerabilidades y Parcheo
* **Riesgo:** Explotación de vulnerabilidades N-Days no mitigadas a tiempo.
* **Recomendaciones:**
  * **SLA de Parcheo:** <7 días para críticas (CVSS > 9), <30 días para altas (Control op.exp.2). (CRÍTICA)
* **Implementación:** Análisis semanal programado con escáner de vulnerabilidades (Nessus/Qualys) → Ventana de maintenance automatizada de SO y Apps nativas.
* **Evidencias (Control Tri-SO):**

| Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
|---|---|---|---|---|
| **Estado Parches** | Panel WSUS o `Get-Hotfix` > 30días | `softwareupdate --history` y estado OS | Reportes `dnf updateinfo` / `apt` patching | Mensual |

### D7. Logging, Auditoría y Detección
* **Riesgo:** Imposibilidad de análisis forense post-incidente por carencia de logs.
* **Recomendaciones:**
  * Recolección centralizada (SIEM) de logs críticos (Fallos Auth, DNS, DHCP, AD, EDR) con 1 año de retención en frío. (CRÍTICA)
* **Implementación:** Sincronizar NTP en todos los activos → Desplegar agentes de log forwarding → Definir alarmas SIEM (ej. accesos en horas inusuales).
* **Evidencias (Control Tri-SO):**

| Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
|---|---|---|---|---|
| **Log Forwarding** | Subscripciones de Windows Event Forwarding (WEF) | Daemon Splunk Forwarder / o `log` nativo redirigido | `auditd` y `rsyslog` forwarding a IP del SIEM | Continuo |

### D8. Backups, Continuidad y Recuperación
* **Riesgo:** Destrucción de datos que provoque quiebra o pérdida catastrófica.
* **Recomendaciones:**
  * Implementar copias de seguridad aisladas y cifradas (inmutables), validando la regla 3-2-1. (CRÍTICA)
  * Pruebas de restauración (DRP) integrales anuales. (ALTA)
* **Implementación:** Clasificar información vital → Aplicar políticas en el agente de backup → Monitoreo diario de éxito.
* **Evidencia:** Logs verdes del software de backup, actas físicas firmadas tras simulacro de recuperación. Frecuencia: Semestral.

### D9. Correo y Colaboración
* **Riesgo:** Infección inicial por phishing, BEC o fuga de información.
* **Recomendaciones:**
  * **Seguridad Dominio:** DMARC (política `p=reject`), SPF (hard fail `-all`) y DKIM activo. (ALTA)
  * **Filtros Avanzados:** Antimalware de mensajería (Advanced Threat Protection) en entrada. (CRÍTICA)
* **Implementación:** Auditar DNS público → Activar sandboxing en Exchange/Google W. → Campañas de Phishing ético simulado.
* **Evidencia:** Reportes DMARC (dmarc-reports), dashboard del ATP bloqueando adjuntos.

### D10. Seguridad Cloud y Configuración
*(No aplica a infraestructura 100% on-premise)*
* **Riesgo:** Exposición pública accidental de contenedores, BBDD o Storage Cuentas Cloud.
* **Recomendaciones:**
  * Integrar herramientas CSPM (Posture Management) para AWS o Azure. (CRÍTICA)
  * Uso estricto de roles de IAM (no claves estáticas compartidas). (ALTA)
* **Implementación:** Check de CIS Foundations en la nube → Habilitar GuardDuty/Defender for Cloud.
* **Evidencia:** Porcentaje "Security Score" en consola cloud > % Objetivo (ej. 85%).

### D11. AppSec / SDLC
* **Riesgo:** Implantación de código propio con vulnerabilidades OWASP Top 10.
* **Recomendaciones:**
  * Integrar escaneos SAST (código fuente) estáticos en el pipeline CI/CD. (MEDIA)
  * Hardening de BBDD backend separando red lógica. (ALTA)
* **Implementación:** Incluir plugins SAST en Jenkins/GitLab → Establecer Quality Gates (fallar build si hay vulnerabilidad Crítica).
* **Evidencias:** Registros de pipelines de CI/CD, reportes DAST en entornos pre-pro.

### D12. Respuesta a Incidentes
* **Riesgo:** Amplificación del impacto económico por falta de procedimiento de comando e incomunicación.
* **Recomendaciones:**
  * Disponer de Playbooks específicos para Ransomware y Brecha de Datos. (ALTA)
  * Realizar un **Tabletop Exercise** (simulacro teórico) anual con la Dirección Técnica. (ALTA)
* **Implementación:** Consolidación de Playbooks → Contratación de soporte de nivel 3 (Retainer IR) → Nombramiento oficial de un equipo de crisis.
* **Evidencia:** Acta resumen del ejercicio Tabletop anual y métricas de MTTR (Mean Time to Recover).

---

## 9. RGPD/LOPDGDD (Aspectos Técnico-Operativos)
Las operaciones técnicas brindan soporte fundamental para el cumplimiento de Protección de Datos Personales (PII).

* **1. Registro de Actividades de Tratamiento (ROPA):**
  Aprobado y supervisado por el DPO. Documentar cada flujo de datos y base legal. IT coopera entregando los mapeos de servidores.
* **2. Evaluación de Impacto (DPIA / EIPD):**
  Establecer checklist (según art. 35 RGPD) que detenga el pase a producción de nuevos proyectos ('Privacy by Design') que traten datos a gran escala o categorías especiales.
* **3. Gestión de Brechas de Seguridad (Notificación 72h):**
  Integración directa del Plan de Incidentes (D12) con el DPO. "Ante compromiso confirmado de confidencialidad, reportar al DPO en 12h, para que éste analice la notificación a la AEPD antes del umbral legal de 72h".
* **4. Acuerdos con Encargados (DPA/SCC):**
  Todo proveedor cloud/TI externo procesando PII debe firmar cláusulas de encargo o Standard Contractual Clauses (SCC) antes de interconexión técnica.
* **5. Retención y Anonimización:**
  Mecanismos técnicos automatizados de purgado legal o seudonimización y cifrado de los repositorios de datos históricos.

---

## Anexo: QA y Verificaciones "SIN EVIDENCIA EN CORPUS"
* **Tri-SO (Check ✓):** Los sistemas Windows, macOS y Linux han sido ponderados igualitariamente en controles y perfiles de Endpoints (D4), Redes (D5), Vulnerabilidades (D6) y Logging (D7).
* **Ausencias / GAPS Documentales:**
  * **SIN EVIDENCIA EN CORPUS:** Marco regulatorio Europeo NIS2 o DORA. (Impacto: Medio. Prioridad de inclusión: Próximo año legislativo).
  * **SIN EVIDENCIA EN CORPUS:** Guías de seguridad OT/SCADA específicas. (Justificación excluidos del Alcance en punto 2).
