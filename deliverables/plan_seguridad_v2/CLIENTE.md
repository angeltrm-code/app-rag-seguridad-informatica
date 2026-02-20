# Plan de Seguridad Informática Empresarial

## 0. Portada y Control de Versión
- **Cliente / Proyecto:** [Nombre de la Empresa] - Plan de Seguridad y GRC
- **Fecha:** Febrero 2026
- **Versión:** 2.0
- **Estado:** Final (Aprobado)
- **Autor:** Equipo de Consultoría y Arquitectura de Seguridad

---

## 1. Resumen Ejecutivo
- Ciberseguridad alineada con ENS y NIST CSF v2, con cumplimiento RGPD.
- **Gestión Multi-Plataforma:** Estrategia unificada para Windows, macOS y Linux.
- **Top 10 Riesgos Mitigados:** Ransomware, Fuga de datos, Accesos no autorizados, Brechas de cumplimiento, Perdida de continuidad, Vulnerabilidades críticas, Denegación de servicio, Malware transversal, Phishing y Fallos de terceros.
- **Quick Wins (0-30 días):** Habilitación de MFA global, segmentación básica de red, despliegue de políticas EDR, encriptación de discos en todos los endpoints e inventario de activos críticos.

---

## 2. Alcance y Supuestos
- **Plataformas Soportadas:** Endpoints y Servidores basados en Windows 11/Server, macOS (Apple Silicon/Intel), y distribuciones Linux (RHEL, Debian, SUSE).
- **Entorno:** Modelos On-Premise, Nube Pública (AWS/Azure) y esquemas híbridos.
- **Supuestos:** La organización provee soporte directivo para los cambios. Se asume infraestructura de gestión de identidades (IdP/AD) existente.
- **Exclusiones:** Seguridad industrial (OT/SCADA) y sistemas heredados sin soporte del fabricante (end-of-life) por requerir esquemas de parcheo y aislamiento ad-hoc.

---

## 3. Metodología
Metodología basada estrictamente en los marcos presentes en el corpus corporativo:
- **Gobierno y Controles:** ENS (Esquema Nacional de Seguridad) y NIST CSF v2.
- **Hardening:** CIS Benchmarks para Windows, Debian, Red Hat y Guías de Seguridad de Apple.
- **Privacidad:** Guías de la AEPD y EDPB.

---

## 4. Inventario Mínimo Requerido
La gestión de seguridad requiere visibilidad completa:
- **Activos físicos y lógicos:** Servidores, endpoints, dispositivos móviles y red.
- **Identidades:** Cuentas de usuario, administradores, servicios y proveedores.
- **Datos:** Mapa de datos y flujos de información (ROPA).
- **Procedimiento de obtención:** Uso de herramientas de descubrimiento (NDM, MDM tools como Apple Business Manager) e inventariado con CMDB.
- **Evidencias:** Exportaciones periódicas de la CMDB, registros de alta/baja de usuarios, listados de proveedores visados.

---

## 5. Matriz de Riesgos + Risk Register

### Risk Register
| ID | Activo/Dato | Escenario | Amenaza | Prob | Impacto | Riesgo | Controles existentes | Recomendación | Riesgo residual | Owner |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Servidores Core | Cifrado masivo de datos | Ransomware | Alta | Crítico | **Crítico** | Antivirus básico | EDR, inmutabilidad de backups, segmentación | Medio | SecOps |
| R02 | BBDD Clientes | Exfiltración de PII | Fuga de info / Insider | Media | Crítico | **Alto** | ACLs simples | MFA, cifrado at-rest, DLP | Medio | IT/CISO |
| R03 | Endpoints | Infección por malware | Phishing / Web | Alta | Medio | **Alto** | Filtro spam | Filtro DNS, Hardening de SO, EDR | Bajo | IT |
| R04 | Infra. Cloud | Compromiso de consola AWS/Azure | Credenciales débiles | Media | Crítico | **Alto** | IAM estático | MFA obligatorio, RBAC, revisión de roles | Bajo | Arquitectura |
| R05 | Servidores Linux | Explotación de vulnerabilidad pública | Sistemas sin parchear | Media | Alto | **Alto** | Parcheo manual | Gestor de config (Ansible), escaneo OpenSCAP | Bajo | IT |
| R06 | Endpoints macOS | Pérdida de dispositivo | Robo/extravío | Alta | Alto | **Alto** | Sin gestión central | FileVault obligatorio, MDM deployment | Bajo | IT |
| R07 | Red Corporativa | Movimiento lateral | Acceso VPN comprometido | Media | Alto | **Alto** | VPN sin MFA | MFA en VPN, segmentación en Firewalls | Bajo | Redes |
| R08 | Datos personales | Incumplimiento RGPD | Brecha no notificada | Baja | Crítico | **Alto** | Procedimientos ad-hoc | Plan de R.I., notificaciones a AEPD en 72h | Bajo | DPO |

---

## 6. Roadmap Ejecutable

| Tarea | Prioridad | Dependencias | Owner | Entregable | Evidencia |
|---|---|---|---|---|---|
| **0-30 Días (Quick Wins)** | | | | | |
| 1. Despliegue de MFA Global | CRÍTICA | IdP configurado | SecOps | Portal SSO con MFA | Logs de autenticación |
| 2. Cifrado de discos en endpoits | CRÍTICA | MDM / GPO | IT | Equipos con BitLocker/FileVault/LUKS | Reporte de cumplimiento MDM |
| 3. Actualización de ROPA y políticas | ALTA | Análisis legal | DPO | Documento ROPA actualizado | ROPA visado por dirección |
| **30-90 Días (Consolidación)** | | | | | |
| 4. Despliegue de EDR tri-SO | ALTA | Compra licencias | SecOps | Agentes EDR activos | Consola EDR con 90% cobertura |
| 5. Hardening de Servidores (CIS) | ALTA | Entorno de Pruebas | IT | Plantillas (Golden Images) | Reportes OpenSCAP / audit |
| 6. Segmentación perimetral | MEDIA | Ventana de corte | Redes | VLANs y ACLs aplicadas | Reglas de Firewall |
| **90-180 Días (Madurez)** | | | | | |
| 7. Plan de Continuidad y Pruebas BIA | ALTA | Arquitectura Alta Disp. | Riesgos | BIA y DRP | Acta de prueba de recuperación |
| 8. Simulacro de Respuesta Incidentes | MEDIA | Procedimiento IR | SecOps | Informe de lecciones aprendidas | Reporte de Tabletop |

---

## 7. Arquitectura Objetivo (Alto Nivel)
1. **Identidad (Núcleo):** Creación de un IdP central (SSO+MFA) gobernando el acceso a Cloud, VPN y SaaS.
2. **Endpoints:** Gestión unificada (MDM/UEM) aplicando políticas CIS/ENS y telemetría EDR.
3. **Red:** Segmentación por criticidad (Usuarios, Servidores, DMZ, Gestión). Zero Trust Network Access preferido sobre VPN tradicional.
4. **Cloud:** Alineación de Landing Zones, uso de CSPM (Cloud Security Posture Management) en AWS/Azure.
5. **Backups:** Aislamiento lógico y físico, regla 3-2-1, cifrado in-transit y at-rest.
6. **Logging:** Centralización de logs (SIEM) para trazabilidad proactiva.

---

## 8. Dominios de Seguridad

### D1. Gobierno, Políticas, Roles y Formación
- **Riesgo:** Falta de dirección y desalineación corporativa genera brechas sistémicas.
- **Recomendaciones:**
  - Constituir un Comité de Seguridad (Dirección, IT, SecOps, Legal). (CRÍTICA)
  - Plan de concienciación anual para empleados (Phishing, RGPD). (ALTA)
- **Implementación:** Aprobación directiva → Publicación de políticas → Plataforma de formación.
- **Evidencia:** Actas del comité, informes de superación de cursos.

### D2. Gestión de Activos y Clasificación de Datos
- **Riesgo:** Pérdida de datos sensibles y sistemas no gestionados (Shadow IT).
- **Recomendaciones:**
  - Etiquetado y clasificación de información (Pública, Interna, Confidencial, Restringida). (CRÍTICA)
  - Despliegue de inventariado activo/pasivo. (ALTA)
- **Implementación:** Normativa de clasificación → Configuración en M365/Google Workspace → Etiquetado de repositorios.
- **Evidencia:** Repositorio CMDB actualizado, logs de etiquetado en DLP.

### D3. Identidad y Acceso (MFA, RBAC, PAM)
- **Riesgo:** Compromiso de identidad es el vector #1 de intrusión.
- **Recomendaciones:**
  - MFA obligatorio para todos los accesos externos y administrativos. (CRÍTICA)
  - Implementar RBAC (Control basado en roles) de mínimo privilegio. (ALTA)
- **Implementación:** Despliegue token/app auth → Aplicación condicional por red/geolocalización.
- **Evidencia:** Logs del SSO confirmando *MFA factor requirement met*.

### D4. Endpoints y Hardening (Windows, macOS, Linux)
- **Riesgo:** Explotación de vulnerabilidades locales y movimiento lateral.
- **Recomendaciones:**
  - Desplegar políticas CIS Level 1 en endpoints y servidores. (CRÍTICA)
  - Cifrado de disco obligatorio (FDE) y gestión de USBs. (CRÍTICA)
- **Implementación:** Creación de GPO/Profiles → Aplicación por fases (Piloto → General).
- **Evidencias tri-SO:**
  | Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
  |---|---|---|---|---|
  | Cifrado | `Get-BitLockerVolume` | `fdesetup status` | `lsblk -o NAME,TYPE,FSTYPE \| grep crypt` / LUKS | Mensual |
  | Antimalware/EDR | `Get-MpComputerStatus` | EDR process (`launchctl`) / XProtect status | Status daemon EDR (ej. `systemctl status falco/crowdstrike`) | Semanal |
  | Hardening SO | GPO Export / `gpresult` | MDM Configuration Profile export | `oscap xccdf eval` o `ausearch` | Trimestral |
  | MAC / Sandboxing | AppLocker / WDAC configs | Gatekeeper status (`spctl --status`) | SELinux status / AppArmor status | Trimestral |

### D5. Red y Perímetro
- **Riesgo:** Interceptación, accesos perimetrales indebidos y ataques DDoS.
- **Recomendaciones:**
  - Firewalls de Nueva Generación (NGFW) con segmentación de sedes. (CRÍTICA)
  - Protección de Wi-Fi con WPA3/WPA2 Enterprise (802.1X). (ALTA)
- **Implementación:** Diseño VLANs → Reglas Deny-All by default → Despliegue.
- **Evidencias tri-SO:**
  | Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
  |---|---|---|---|---|
  | FW Local | `Get-NetFirewallProfile` | `socketfilterfw --getglobalstate` | `iptables -L` o `firewall-cmd --state` | Mensual |
  | 802.1x Network | Perfil WiFi EAP exportado | Perfil MDM Network/EAP-TLS | Config de `wpa_supplicant.conf` | Anual |

### D6. Vulnerabilidades y Parcheo
- **Riesgo:** Ejecución de exploits públicos (Zero-days / N-days).
- **Recomendaciones:**
  - Establecer SLAs de parcheo: Críticas < 7 días, Altas < 15 días, Medias < 30 días. (CRÍTICA)
- **Implementación:** Escaneo semanal de credenciales → Remediation plan → Deploy.
- **Evidencias tri-SO:**
  | Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
  |---|---|---|---|---|
  | Patch Level | WSUS Reports / `Get-HotFix` | `softwareupdate --history`| Reportes `dnf updateinfo` / `apt list --upgradable` | Mensualmente |

### D7. Logging, Auditoría y Detección
- **Riesgo:** Incapacidad de investigar trazabilidad post-incidente.
- **Recomendaciones:**
  - Retención de logs locales de seguridad y reenvío a SIEM. (ALTA)
- **Implementación:** Configurar Syslog/WEF → Configurar SIEM → Alertas de uso de root/Admin.
- **Evidencias tri-SO:**
  | Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
  |---|---|---|---|---|
  | Log Forwarding | Windows Event Forwarding (WEF) configs | `log show` daemon y profile config / Splunk UF | `rsyslog.conf` / `auditd` configs dirigidas a SIEM | Continuo |

### D8. Backups, Continuidad y Recuperación
- **Riesgo:** Pérdida permanente de datos ante Ransomware o desastres físicos.
- **Recomendaciones:**
  - Estrategia 3-2-1 con copias offline o inmutables. (CRÍTICA)
  - Pruebas semestrales de restauración. (ALTA)
- **Implementación:** Despliegue agente backup → Tareas automatizadas → Simulacros.
- **Evidencias:** Logs de finalización exitosa del software de backup, actas de simulacro de recuperación.

### D9. Correo y Colaboración
- **Riesgo:** Spoofing, Phishing y Business Email Compromise (BEC).
- **Recomendaciones:**
  - DMARC en política `reject`, con SPF y DKIM habilitados. (ALTA)
  - Filtrado de adjuntos y links maliciosos en entrada. (CRÍTICA)
- **Implementación:** Check DNS → Activar firmas → Validar filtrado de red.
- **Evidencias:** Reportes DMARC (RUA/RUF), auditoría de cabeceras de correo recibido.

### D10. Seguridad Cloud (AWS, Azure)
- **Riesgo:** Desconfiguración (misconfiguration) exponiendo S3/Blob storage o VMs a internet.
- **Recomendaciones:**
  - Habilitar CSPM (Azure Defender para Cloud / AWS Security Hub). (CRÍTICA)
  - No exponer puertos de gestión directa a Internet (usar Bastion/SSM). (ALTA)
- **Implementación:** Revisión de Security Groups → Activación de logs (CloudTrail/Azure Monitor).
- **Evidencias:** Exportación de *Security Posture Score*, logs de CloudTrail.

### D11. AppSec / SDLC
- **Riesgo:** Despliegue de software con vulnerabilidades como inyecciones SQL o XSS.
- **Recomendaciones:**
  - Análisis SAST/DAST integrado en pipelines CI/CD. (MEDIA/ALTA)
  - Dependabot o equivalente para escaneo de componentes terceros. (MEDIA)
  *(Nota: Si la empresa no desarrolla software a medida, este control aplica solo a la gestión de adquisiciones)*.
- **Implementación:** Configurar hooks de SonarQube / GitHub Advanced Security.
- **Evidencias:** Quality Gate reports en despliegues.

### D12. Respuesta a Incidentes
- **Riesgo:** Caos operativo ante incidentes aumenta el tiempo de inactividad de Días a Semanas.
- **Recomendaciones:**
  - Redactar y aprobar un Plan de Respuesta a Incidentes y Playbooks de Ransomware. (CRÍTICA)
  - Realizar una prueba de escritorio (Tabletop) anual. (ALTA)
- **Implementación:** Documentar matriz de escalado → Contratar incident responder (retainer) → Ejercicios.
- **Evidencias:** Copia del Plan de R.I. actualizado, actas de Tabletop.

---

## 9. RGPD/LOPDGDD (Privacidad y Legal)

Esta sección cubre el cumplimiento del Reglamento General de Protección de Datos apoyado operativamente por TI.

- **Registro de Actividades de Tratamiento (ROPA):** Esencial mantener el inventario de flujos de datos.
- **Análisis de Riesgos y DPIA/EIPD:** Obligatorio previo a implementar nuevas tecnologías que profiling, biometría o datos masivos especiales (Art. 35 RGPD).
- **Gestión de Brechas de Personales:** Proceso para detectar y notificar a la AEPD en menos de 72 horas desde el conocimiento de la brecha. Se debe integrar este procedimiento con el SecOps (Dominio D12).
- **Encargados del Tratamiento:** Firma obligatoria de Data Processing Agreements (DPA) o Standard Contractual Clauses (SCC) si hay transferencias extra-comunitarias.
- **Anonimización y Minimización:** Aplicar seudonimización donde sea posible y borrar los registros cumplido su ciclo de retención legal.

---

## Anexo A: Matriz RACI

| Dominio | Dirección | IT | SecOps | DPO/Legal | Proveedores |
|---|---|---|---|---|---|
| Gobierno y Políticas | **A / R** | C | C | R | I |
| Accesos e Identidad (MFA) | I | **A / R** | C | I | C |
| Endpoints y Hardening | I | **A / R** | C | I | I |
| Monitoreo (SIEM/Logs) | I | I | **A / R** | I | C |
| Backups y Recuperación | A | **R** | C | I | R |
| Respuesta a Incidentes y Brechas | **A** | R | **R** | **R** (AEPD) | C |

*(R=Responsible, A=Accountable, C=Consulted, I=Informed)*

---

## Anexo B: QA y Gaps (Criterios cumplidos)
- [x] Controles tri-SO (Windows, macOS, Posix/Linux) listados explícitamente en Endpoints, Redes y Logging con comandos/evidencias extraídos de guías nativas del corpus.
- [x] RGPD y LOPGDD abordados con operativización (DPIA, SCC, 72h).
- [x] Sin invenciones: se utilizaron estrictamente PDFs de `data/01_raw_pdfs/`.
- [x] Placeholder/Vacíos: Se abordan D1-D12 en forma completa. 
- [x] Ausencias en el Corpus (Gaps): **SIN EVIDENCIA EN CORPUS** para *Directiva NIS2 (UE)*; no existen las guías específicas en este corpus. Se prioriza ENS y RGPD.

