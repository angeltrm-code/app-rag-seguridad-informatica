# Plan de Seguridad Informática Empresarial
**Nivel:** Estratégico y Operativo (vCISO)
**Audiencia:** Internal (Con trazabilidad a fuentes primarias del corpus corporativo)

## 0. Portada y Control de Versión
* **Cliente / Proyecto:** [Nombre de Empresa] - Transformación en Ciberseguridad GRC
* **Fecha:** Febrero 2026
* **Versión:** 2.0 (Tri-SO & RGPD)
* **Estado:** FINAL
* **Autor:** Equipo vCISO y Arquitectura de Seguridad

---

## 1. Resumen Ejecutivo
Este plan estratégico establece los cimientos defensivos y normativos para [Nombre de Empresa], fundamentado en los controles de ENS [05-ens_medidas_implantacion.pdf], NIST CSF v2 [07-nist_csf_v2.pdf], y la legislación de protección de datos (RGPD/LOPDGDD) [93-guia-rgpd-para-responsables-de-tratamiento.pdf].

* **Top Riesgos Identificados:** 1) Infección por Ransomware [22-ransomware_incidentes_ccn.pdf], 2) Fuga de Información PII [24-fuga_informacion.pdf], 3) Movimiento lateral desde endpoints comprometidos [40-endpoint_seguro.pdf], 4) Accesos cloud no autorizados [99-azure-security-documentation.pdf], 5) Pérdida de continuidad de negocio.
* **Quick Wins (0–30 días):** 
  * Despliegue de MFA forzado para accesos VPN y Cloud [27-identidad_digital_ciberseguridad.pdf].
  * Cifrado de discos en el 100% del parque (BitLocker/FileVault/LUKS).
  * Despliegue de EDR base en endpoints [40-endpoint_seguro.pdf].
  * Actualización del Registro de Actividades de Tratamiento (ROPA) [123-guia-listado-de-cumplimiento-del-rgpd.pdf].

---

## 2. Alcance y Supuestos
* **Entornos Cubiertos:** Endpoints y Servidores. Operación On-Premise y Cloud Híbrido (AWS/Azure) [96-aws_security_best_practices.pdf].
* **Plataformas Homologadas (Tri-SO):** 
  * Windows 11 / Windows Server 2022 o superior.
  * macOS (Apple Silicon e Intel soportado) [50-apple_platform_security.pdf].
  * Linux (RHEL 9, Debian 12, SLES) [86-book-security_en.pdf].
* **Supuestos:** Apoyo explícito de Dirección General mediante un Comité de Seguridad [15-plan_director_seguridad.pdf]. Centralización de identidades en Active Directory / Entra ID.
* **Exclusiones:** Sistemas industriales (OT) y sistemas operativos obsoletos o sin soporte del fabricante; estos se segregarán en redes aisladas (air-gapped) o micro-segmentadas.

---

## 3. Metodología
Las recomendaciones derivan exclusivamente de las siguientes referencias normativas (Corpus Documental Cerrado SSoT):
* **Gobernanza:** Esquema Nacional de Seguridad (ENS) [06-ens_declaracion_aplicabilidad.pdf].
* **Framework Arquitectura:** NIST CSF v2 [07-nist_csf_v2.pdf].
* **Privacidad (GRC):** Guías AEPD y EDPB [89-edpb_guidelines_201904_dataprotection_by_design_and_by_defau.pdf].
* **Hardening Técnico:** CIS Benchmarks [42-windows11_cis_benchmark.pdf] [105-cis_debian_linux_12_benchmark_v1_1_0.pdf], Guías Apple [73-managing_devices_and_corporate_data_on_ios.pdf] y Red Hat/SUSE [77-red_hat_enterprise_linux-9-security_hardening-en-us.pdf].

---

## 4. Inventario Mínimo Requerido
La gestión de activos es el núcleo fundacional. "No se puede proteger lo que no se conoce" [05-ens_medidas_implantacion.pdf] (Control op.act.1).
* **Activos:** Hardware (laptops, servers, móviles) [48-mdm_gestion_dispositivos.pdf] y Software (licencias, SaaS).
* **Identidades:** Empleados, contractors, identidades de servicio (M2M).
* **Datos:** Clasificación de la información corporativa [29-etiquetas_seguridad.pdf].
* **Procedimiento:** Integración de herramientas de MDM (Intune/Jamf/Apple Business Manager [70-apple_business_manager_getting_started_guide.pdf]) con herramienta ITSM (CMDB).
* **Evidencias Generadas:** Reporte de cobertura del MDM/CMDB mensual.

---

## 5. Matriz de Riesgos + Risk Register

| ID | Activo/Dato | Escenario | Amenaza | Prob | Impacto | Riesgo | Controles existentes | Recomendación | Riesgo residual | Owner |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Servidores Core | Cifrado masivo de datos e indisponibilidad | Ransomware / Cibercrimen [22-ransomware_incidentes_ccn.pdf] | Alta | Crítico | **Crítico** | Antivirus legacy | EDR avanzado, inmutabilidad de backups intra-red | Medio | SecOps |
| R02 | BBDD y Repositorios | Exfiltración de PII de clientes | Insider / Exfiltración [24-fuga_informacion.pdf] | Media | Crítico | **Alto** | Permisos laxos NTFS/S3 | MFA, RBAC, Cifrado at-rest, DLP | Bajo | IT |
| R03 | Todos los Endpoints | Infección por malware transversal | Phishing / Web surfing [40-endpoint_seguro.pdf] | Alta | Alto | **Alto** | Sin filtrado perimetral | Filtro DNS, EDR, Hardening Tri-SO (CIS) | Bajo | IT |
| R04 | Cuentas Privilegiadas Cloud | Compromiso de panel de control cloud | Credenciales débiles expuestas [99-azure-security-documentation.pdf] | Alta | Crítico | **Crítico** | Autenticación simple | MFA universal, PAM para administradores (JIT) | Bajo | Arquitect. |
| R05 | Servidores Linux / DMZ | Explotación de RCE por vulnerabilidad pública | Parcheo deficiente [84-article-openscap_en.pdf] | Media | Alto | **Alto** | Parcheo reactivo anual | Gestor de config central (Ansible) + escaneo SCAP | Bajo | IT |
| R06 | Endpoints macOS / Portátiles | Extravío de dispositivo local | Robo físico [50-apple_platform_security.pdf] | Alta | Alto | **Alto** | Claves simples, sin cifrado | FileVault forzado, MDM con remote-wipe | Bajo | IT |
| R07 | Entorno Windows | Elevación de privilegios locales | Movimiento lateral [42-windows11_cis_benchmark.pdf] | Alta | Alto | **Alto** | Usuarios son Admin Locales | Retirar Admin Local, LAPS, AppLocker base | Bajo | IT / SecOps |
| R08 | Datos Personales (RH) | Incumplimiento sanciones RGPD | Brecha no notificada (72h) [90-edpb_guidelines_202209_personal_data_breach_notification_v2.pdf] | Baja | Crítico | **Alto** | Sin proceso de RI | Establecer playbooks IR, contacto directo DPO | Bajo | DPO / IR |

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
1. **Identidad (El nuevo perímetro):** SSO y MFA para todos los sistemas (Zero Trust fundamentals) [27-identidad_digital_ciberseguridad.pdf].
2. **Endpoints:** Terminales inmutables y gestionados por MDM (Jamf, Intune, Workspace ONE) [48-mdm_gestion_dispositivos.pdf].
3. **Red:** Segmentación estricta separando estaciones de trabajo, servidores (DMZ vs Backend) y gestión [16-principios_recomendaciones_basicas.pdf].
4. **Cloud:** Uso de Landing Zones seguras, cifrado de repositorios S3/Blob, y evaluación de CSPM continuo [96-aws_security_best_practices.pdf].
5. **Backups:** Arquitectura 3-2-1, almacenamiento offline o inmutable, y cifrado out-of-band [57-copias_seguridad.pdf].

---

## 8. Dominios de Seguridad (D1 - D12)

### D1. Gobierno, Políticas, Roles y Formación
* **Riesgo:** El desconocimiento de la normatividad interna causa exposición.
* **Recomendaciones:**
  * Conformar un **Comité de Ciberseguridad** (Dirección, CISO, Legal, IT) con reuniones trimestrales [15-plan_director_seguridad.pdf]. (CRÍTICA)
  * Capacitación obligatoria trianual en Anti-Phishing y Privacidad [69-concienciacion_formacion.pdf]. (ALTA)
* **Implementación:** 1. Redactar borrador de Política General. 2. Firmar por gerencia. 3. Lanzar plataforma LMS.
* **Evidencia:** Actas del comité, certificados de superación de cursos. Frecuencia: Anual.

### D2. Gestión de Activos y Clasificación de Datos
* **Riesgo:** Shadow IT y exposición de PII sin control de acceso.
* **Recomendaciones:**
  * Implementar taxonomía de etiquetas (Ej. *Público, Uso Interno, Confidencial*) en la suite ofimática [29-etiquetas_seguridad.pdf]. (CRÍTICA)
* **Implementación:** Definición en comité → Configuración DLP/AIP → Capacitación.
* **Evidencia:** Repositorio en el MDM/CMDB, reglas DLP activas mapeando las etiquetas confidenciales.

### D3. Identidad y Acceso (IAM)
* **Riesgo:** Credenciales expuestas llevan a compromiso total de dominio.
* **Recomendaciones:**
  * **MFA obligatorio** para todos los accesos externos, VPN y cuentas con privilegios administrativos [27-identidad_digital_ciberseguridad.pdf]. (CRÍTICA)
  * **Mínimo Privilegio (RBAC):** Eliminar cuentas genéricas compartidas y usar Privileged Access Management (PAM) [05-ens_medidas_implantacion.pdf]. (ALTA)
* **Implementación:** Activar Conditional Access Policies en IdP → Auditar cuentas huérfanas mensualmente.
* **Evidencia:** Exportación del IdP mostrando MFA _Enforced_ en un 100% de VPN/Admins.

### D4. Endpoints y Hardening (Tri-SO)
* **Riesgo:** Infección por malware y movimiento lateral entre sistemas operativos.
* **Recomendaciones:**
  * **Hardening Base:** Aplicar perfiles CIS Benchmarks Nivel 1 [42-windows11_cis_benchmark.pdf] [105-cis_debian_linux_12_benchmark_v1_1_0.pdf]. (ALTA)
  * **Cifrado de Disco Completo (FDE)** [40-endpoint_seguro.pdf]. (CRÍTICA)
* **Implementación:** Pilot testing de GPOs/Perfiles MDM → Despliegue masivo → Monitoreo vía SCAP.
* **Evidencias (Control Tri-SO):**

| Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
|---|---|---|---|---|
| **Cifrado (FDE)** | `manage-bde -status` o logs Intune [40-endpoint_seguro.pdf] | `fdesetup status` habilitado [50-apple_platform_security.pdf] | Volumen cifrado LUKS activo (`lsblk`) [87-debian-handbook.pdf] | Quincenal |
| **EDR / AV** | Security Center: Defender Running [82-windows-defender-evaluation-guide.pdf] | Agente EDR activo via MDM System Extension | Servicio local EDR `systemctl status <edr>` | Continuo |
| **Hardening SO** | Reporte CIS / GPO Compliance report | Exportación perfiles `.mobileconfig` MDM [73-managing_devices_and_corporate_data_on_ios.pdf] | Scaneos OpenSCAP pass rate [84-article-openscap_en.pdf] | Trimestral |
| **Control Periférico**| Políticas USB deshabilitado [40-endpoint_seguro.pdf] | Restricción de Media via MDM Payload | Reglas `udev` de bloqueo de almacenamiento [110-sles-selinux_en.pdf] | Semestral |

### D5. Red y Perímetro
* **Riesgo:** Acceso irrestricto de atacantes a redes core mediante pivoting.
* **Recomendaciones:**
  * **Segmentación Lógica:** Redes separadas para Visitas, Empleados, IoT, y Servidores mediante NGFW [33-proteccion_dos_cortafuegos.pdf]. (CRÍTICA)
  * **Cifrado In-Transit:** Forzar WPA3 o WPA2-Enterprise para Wi-Fi [35-seguridad_redes_wifi.pdf], terminación TLS 1.2+ en webservers [32-https_seguridad.pdf]. (ALTA)
* **Implementación:** Revisión de arquitectura de red → Ajuste de VLANs → Habilitar ACLs Default-Deny.
* **Evidencias (Control Tri-SO):**

| Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
|---|---|---|---|---|
| **Firewall Host** | `Get-NetFirewallProfile` (Activo) | Perfil local `socketfilterfw` activo | `firewalld` o `ufw` enabled [78-red_hat_enterprise_linux-9-securing_networks-en-us.pdf] | Mensual |
| **Acceso Red (NAC)**| Certificados EAP-TLS en MMC | Payload Network MDM de tipo TLS | Config de `wpa_supplicant` / cert local | Anual |

### D6. Vulnerabilidades y Parcheo
* **Riesgo:** Explotación de vulnerabilidades N-Days no mitigadas a tiempo.
* **Recomendaciones:**
  * **SLA de Parcheo:** <7 días para críticas (CVSS > 9), <30 días para altas [05-ens_medidas_implantacion.pdf] (Control op.exp.2). (CRÍTICA)
* **Implementación:** Análisis semanal programado con escáner de vulnerabilidades (Nessus/Qualys) → Ventana de maintenance automatizada de SO y Apps nativas.
* **Evidencias (Control Tri-SO):**

| Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
|---|---|---|---|---|
| **Estado Parches** | Panel WSUS o `Get-Hotfix` > 30días | `softwareupdate --history` y estado OS [73-managing_devices_and_corporate_data_on_ios.pdf] | Reportes `dnf updateinfo` / `apt` patching [105-cis_debian_linux_12_benchmark_v1_1_0.pdf] | Mensual |

### D7. Logging, Auditoría y Detección
* **Riesgo:** Imposibilidad de análisis forense post-incidente por carencia de logs.
* **Recomendaciones:**
  * Recolección centralizada (SIEM) de logs críticos (Fallos Auth, DNS, DHCP, AD, EDR) con 1 año de retención en frío [16-principios_recomendaciones_basicas.pdf]. (CRÍTICA)
* **Implementación:** Sincronizar NTP en todos los activos → Desplegar agentes de log forwarding → Definir alarmas SIEM (ej. accesos en horas inusuales).
* **Evidencias (Control Tri-SO):**

| Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
|---|---|---|---|---|
| **Log Forwarding** | Subscripciones de Windows Event Forwarding (WEF) [81-windows_event_logging_and_forwarding_october_2021.pdf] | Daemon Splunk Forwarder / o `log` nativo redirigido | `auditd` y `rsyslog` forwarding a IP del SIEM [74-ol8-auditing.pdf] [77-red_hat_enterprise_linux-9-security_hardening-en-us.pdf] | Continuo |

### D8. Backups, Continuidad y Recuperación
* **Riesgo:** Destrucción de datos que provoque quiebra o pérdida catastrófica.
* **Recomendaciones:**
  * Implementar copias de seguridad aisladas y cifradas (inmutables), validando la regla 3-2-1 [57-copias_seguridad.pdf]. (CRÍTICA)
  * Pruebas de restauración (DRP) integrales anuales. (ALTA)
* **Implementación:** Clasificar información vital → Aplicar políticas en el agente de backup → Monitoreo diario de éxito.
* **Evidencia:** Logs verdes del software de backup, actas físicas firmadas tras simulacro de recuperación [11-pilar_impacto_continuidad.pdf]. Frecuencia: Semestral.

### D9. Correo y Colaboración
* **Riesgo:** Infección inicial por phishing, BEC o fuga de información.
* **Recomendaciones:**
  * **Seguridad Dominio:** DMARC (política `p=reject`), SPF (hard fail `-all`) y DKIM activo [31-correo_dmarc.pdf]. (ALTA)
  * **Filtros Avanzados:** Antimalware de mensajería (Advanced Threat Protection) en entrada [30-correo_electronico_seguridad.pdf]. (CRÍTICA)
* **Implementación:** Auditar DNS público → Activar sandboxing en Exchange/Google W. → Campañas de Phishing ético simulado.
* **Evidencia:** Reportes DMARC (dmarc-reports), dashboard del ATP bloqueando adjuntos.

### D10. Seguridad Cloud y Configuración
*(No aplica a infraestructura 100% on-premise)*
* **Riesgo:** Exposición pública accidental de contenedores, BBDD o Storage Cuentas Cloud.
* **Recomendaciones:**
  * Integrar herramientas CSPM (Posture Management) para AWS o Azure [99-azure-security-documentation.pdf] [96-aws_security_best_practices.pdf]. (CRÍTICA)
  * Uso estricto de roles de IAM (no claves estáticas compartidas) [96-aws_security_best_practices.pdf]. (ALTA)
* **Implementación:** Check de CIS Foundations en la nube → Habilitar GuardDuty/Defender for Cloud.
* **Evidencia:** Porcentaje "Security Score" en consola cloud > % Objetivo (ej. 85%).

### D11. AppSec / SDLC
* **Riesgo:** Implantación de código propio con vulnerabilidades OWASP Top 10.
* **Recomendaciones:**
  * Integrar escaneos SAST (código fuente) estáticos en el pipeline CI/CD [62-desarrollo_seguro.pdf]. (MEDIA)
  * Hardening de BBDD backend separando red lógica [65-bbdd_seguridad_general.pdf]. (ALTA)
* **Implementación:** Incluir plugins SAST en Jenkins/GitLab → Establecer Quality Gates (fallar build si hay vulnerabilidad Crítica).
* **Evidencias:** Registros de pipelines de CI/CD, reportes DAST en entornos pre-pro.

### D12. Respuesta a Incidentes
* **Riesgo:** Amplificación del impacto económico por falta de procedimiento de comando e incomunicación.
* **Recomendaciones:**
  * Disponer de Playbooks específicos para Ransomware y Brecha de Datos [20-gestion_crisis_incibe.pdf]. (ALTA)
  * Realizar un **Tabletop Exercise** (simulacro teórico) anual con la Dirección Técnica [22-ransomware_incidentes_ccn.pdf]. (ALTA)
* **Implementación:** Consolidación de Playbooks → Contratación de soporte de nivel 3 (Retainer IR) → Nombramiento oficial de un equipo de crisis.
* **Evidencia:** Acta resumen del ejercicio Tabletop anual y métricas de MTTR (Mean Time to Recover).

---

## 9. RGPD/LOPDGDD (Aspectos Técnico-Operativos)
Las operaciones técnicas brindan soporte fundamental para el cumplimiento de Protección de Datos Personales (PII).

* **1. Registro de Actividades de Tratamiento (ROPA):**
  Aprobado y supervisado por el DPO. Documentar cada flujo de datos y base legal [93-guia-rgpd-para-responsables-de-tratamiento.pdf]. IT coopera entregando los mapeos de servidores.
* **2. Evaluación de Impacto (DPIA / EIPD):**
  Establecer checklist (según art. 35 RGPD) que detenga el pase a producción de nuevos proyectos ('Privacy by Design') que traten datos a gran escala o categorías especiales [89-edpb_guidelines_201904_dataprotection_by_design_and_by_defau.pdf] [91-gestion-riesgo-y-evaluacion-impacto-en-tratamientos-datos-pe.pdf].
* **3. Gestión de Brechas de Seguridad (Notificación 72h):**
  Integración directa del Plan de Incidentes (D12) con el DPO. "Ante compromiso confirmado de confidencialidad, reportar al DPO en 12h, para que éste analice la notificación a la AEPD antes del umbral legal de 72h" [90-edpb_guidelines_202209_personal_data_breach_notification_v2.pdf] [94-guia_nacional_notificacion_gestion_ciberincidentes.pdf].
* **4. Acuerdos con Encargados (DPA/SCC):**
  Todo proveedor cloud/TI externo procesando PII debe firmar cláusulas de encargo o Standard Contractual Clauses (SCC) antes de interconexión técnica [138-si_sa_standard_contract_clauses_en.pdf].
* **5. Retención y Anonimización:**
  Mecanismos técnicos automatizados de purgado legal o seudonimización y cifrado de los repositorios de datos históricos [125-guia-orientaciones-procedimientos-anonimizacion.pdf].

---

## Anexo: QA y Verificaciones "SIN EVIDENCIA EN CORPUS"
* **Tri-SO (Check ✓):** Los sistemas Windows, macOS y Linux han sido ponderados igualitariamente en controles y perfiles de Endpoints (D4), Redes (D5), Vulnerabilidades (D6) y Logging (D7).
* **Ausencias / GAPS Documentales:**
  * **SIN EVIDENCIA EN CORPUS:** Marco regulatorio Europeo NIS2 o DORA. (Impacto: Medio. Prioridad de inclusión: Próximo año legislativo).
  * **SIN EVIDENCIA EN CORPUS:** Guías de seguridad OT/SCADA específicas. (Justificación excluidos del Alcance en punto 2).
