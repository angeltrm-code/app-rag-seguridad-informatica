import re

internal_content = """# Plan de Seguridad Informática Empresarial
**Nivel:** Generalista (Adaptable a PYME y Gran Empresa)

## 0. Portada y Control de Versión
- **Cliente / Proyecto:** [Nombre de la Empresa] - Plan de Seguridad y GRC
- **Fecha:** Febrero 2026
- **Versión:** 2.0
- **Estado:** Final (Aprobado)
- **Autor:** Equipo de Consultoría y Arquitectura de Seguridad

---

## 1. Resumen Ejecutivo
- Ciberseguridad alineada con ENS [05-ens_medidas_implantacion.pdf] y NIST CSF v2 [07-nist_csf_v2.pdf], con cumplimiento RGPD [93-guia-rgpd-para-responsables-de-tratamiento.pdf].
- **Gestión Multi-Plataforma:** Estrategia unificada para Windows, macOS y Linux.
- **Top 10 Riesgos Mitigados:** Ransomware [22-ransomware_incidentes_ccn.pdf], Fuga de datos [24-fuga_informacion.pdf], Accesos no autorizados [30-correo_electronico_seguridad.pdf], Brechas de cumplimiento, Perdida de continuidad, Vulnerabilidades críticas, Denegación de servicio, Malware transversal, Phishing y Fallos de terceros.
- **Quick Wins (0-30 días):** Habilitación de MFA global, segmentación básica de red, despliegue de políticas EDR [40-endpoint_seguro.pdf], encriptación de discos en todos los endpoints e inventario de activos críticos.

---

## 2. Alcance y Supuestos
- **Plataformas Soportadas:** Endpoints y Servidores basados en Windows 11/Server, macOS (Apple Silicon/Intel), y distribuciones Linux (RHEL, Debian, SUSE) [86-book-security_en.pdf] [50-apple_platform_security.pdf] [72-msft-windows11-security-book_sept2023.pdf].
- **Entorno:** Modelos On-Premise, Nube Pública (AWS/Azure) [96-aws_security_best_practices.pdf] y esquemas híbridos.
- **Supuestos:** La organización provee soporte directivo para los cambios [15-plan_director_seguridad.pdf]. Se asume infraestructura de gestión de identidades (IdP/AD) existente.
- **Exclusiones:** Seguridad industrial (OT/SCADA) y sistemas heredados sin soporte del fabricante (end-of-life) por requerir esquemas de parcheo y aislamiento ad-hoc [58-iot_seguridad.pdf].

---

## 3. Metodología
Metodología basada estrictamente en los marcos presentes en el corpus corporativo:
- **Gobierno y Controles:** ENS (Esquema Nacional de Seguridad) [05-ens_medidas_implantacion.pdf] y NIST CSF v2 [07-nist_csf_v2.pdf].
- **Hardening:** CIS Benchmarks para Windows [42-windows11_cis_benchmark.pdf], Debian [105-cis_debian_linux_12_benchmark_v1_1_0.pdf], Red Hat [106-cis_rhlinux_benchmark_v105.pdf] y Guías de Seguridad de Apple [50-apple_platform_security.pdf].
- **Privacidad:** Guías de la AEPD y EDPB [119-edpb-summary-gdpr-data-protection-design-default_en.pdf].

---

## 4. Inventario Mínimo Requerido
La gestión de seguridad requiere visibilidad completa [05-ens_medidas_implantacion.pdf]:
- **Activos físicos y lógicos:** Servidores, endpoints, dispositivos móviles y red.
- **Identidades:** Cuentas de usuario, administradores, servicios y proveedores.
- **Datos:** Mapa de datos y flujos de información (ROPA) [93-guia-rgpd-para-responsables-de-tratamiento.pdf].
- **Procedimiento de obtención:** Uso de herramientas de descubrimiento (NDM, MDM tools como Apple Business Manager [70-apple_business_manager_getting_started_guide.pdf]) e inventariado con CMDB.
- **Evidencias:** Exportaciones periódicas de la CMDB, registros de alta/baja de usuarios, listados de proveedores visados.

---

## 5. Matriz de Riesgos + Risk Register

### Risk Register
| ID | Activo/Dato | Escenario | Amenaza | Prob | Impacto | Riesgo | Controles existentes | Recomendación | Riesgo residual | Owner |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Servidores Core | Cifrado masivo de datos | Ransomware [22-ransomware_incidentes_ccn.pdf] | Alta | Crítico | **Crítico** | Antivirus básico | EDR, inmutabilidad de backups, segmentación | Medio | SecOps |
| R02 | BBDD Clientes | Exfiltración de PII | Fuga de info / Insider [24-fuga_informacion.pdf] | Media | Crítico | **Alto** | ACLs simples | MFA, cifrado at-rest, DLP | Medio | IT/CISO |
| R03 | Endpoints | Infección por malware | Phishing / Web [40-endpoint_seguro.pdf] | Alta | Medio | **Alto** | Filtro spam | Filtro DNS, Hardening de SO, EDR | Bajo | IT |
| R04 | Infra. Cloud | Compromiso de consola AWS/Azure | Credenciales débiles [96-aws_security_best_practices.pdf] | Media | Crítico | **Alto** | IAM estático | MFA obligatorio, RBAC, revisión de roles | Bajo | Arquitectura |
| R05 | Servidores Linux | Explotación de vulnerabilidad pública | Sistemas sin parchear [84-article-openscap_en.pdf] | Media | Alto | **Alto** | Parcheo manual | Gestor de config (Ansible), escaneo OpenSCAP | Bajo | IT |
| R06 | Endpoints macOS | Pérdida de dispositivo | Robo/extravío [50-apple_platform_security.pdf] | Alta | Alto | **Alto** | Sin gestión central | FileVault obligatorio, MDM deployment | Bajo | IT |
| R07 | Red Corporativa | Movimiento lateral | Acceso VPN comprometido [16-principios_recomendaciones_basicas.pdf] | Media | Alto | **Alto** | VPN sin MFA | MFA en VPN, segmentación en Firewalls | Bajo | Redes |
| R08 | Datos personales | Incumplimiento RGPD | Brecha no notificada [90-edpb_guidelines_202209_personal_data_breach_notification_v2.pdf] | Baja | Crítico | **Alto** | Procedimientos ad-hoc | Plan de R.I., notificaciones a AEPD en 72h | Bajo | DPO |

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
1. **Identidad (Núcleo):** Creación de un IdP central (SSO+MFA) gobernando el acceso a Cloud, VPN y SaaS [27-identidad_digital_ciberseguridad.pdf].
2. **Endpoints:** Gestión unificada (MDM/UEM) aplicando políticas CIS/ENS y telemetría EDR [48-mdm_gestion_dispositivos.pdf].
3. **Red:** Segmentación por criticidad (Usuarios, Servidores, DMZ, Gestión) [16-principios_recomendaciones_basicas.pdf]. Zero Trust Network Access preferido sobre VPN tradicional.
4. **Cloud:** Alineación de Landing Zones, uso de CSPM (Cloud Security Posture Management) en AWS/Azure [99-azure-security-documentation.pdf].
5. **Backups:** Aislamiento lógico y físico, regla 3-2-1, cifrado in-transit y at-rest [57-copias_seguridad.pdf].
6. **Logging:** Centralización de logs (SIEM) para trazabilidad proactiva [81-windows_event_logging_and_forwarding_october_2021.pdf].

---

## 8. Dominios de Seguridad

### D1. Gobierno, Políticas, Roles y Formación
- **Riesgo:** Falta de dirección y desalineación corporativa genera brechas sistémicas.
- **Recomendaciones:**
  - Constituir un Comité de Seguridad (Dirección, IT, SecOps, Legal) [15-plan_director_seguridad.pdf]. (CRÍTICA)
  - Plan de concienciación anual para empleados (Phishing, RGPD) [69-concienciacion_formacion.pdf]. (ALTA)
- **Implementación:** Aprobación directiva → Publicación de políticas → Plataforma de formación.
- **Evidencia:** Actas del comité, informes de superación de cursos.

### D2. Gestión de Activos y Clasificación de Datos
- **Riesgo:** Pérdida de datos sensibles y sistemas no gestionados (Shadow IT).
- **Recomendaciones:**
  - Etiquetado y clasificación de información (Pública, Interna, Confidencial, Restringida) [29-etiquetas_seguridad.pdf]. (CRÍTICA)
  - Despliegue de inventariado activo/pasivo. (ALTA)
- **Implementación:** Normativa de clasificación → Configuración en M365/Google Workspace → Etiquetado de repositorios.
- **Evidencia:** Repositorio CMDB actualizado, logs de etiquetado en DLP.

### D3. Identidad y Acceso (MFA, RBAC, PAM)
- **Riesgo:** Compromiso de identidad es el vector #1 de intrusión.
- **Recomendaciones:**
  - MFA obligatorio para todos los accesos externos y administrativos [27-identidad_digital_ciberseguridad.pdf]. (CRÍTICA)
  - Implementar RBAC (Control basado en roles) de mínimo privilegio [05-ens_medidas_implantacion.pdf]. (ALTA)
- **Implementación:** Despliegue token/app auth → Aplicación condicional por red/geolocalización.
- **Evidencia:** Logs del SSO confirmando *MFA factor requirement met*.

### D4. Endpoints y Hardening (Windows, macOS, Linux)
- **Riesgo:** Explotación de vulnerabilidades locales y movimiento lateral.
- **Recomendaciones:**
  - Desplegar políticas CIS Level 1 en endpoints y servidores. (CRÍTICA)
  - Cifrado de disco obligatorio (FDE) y gestión de USBs [40-endpoint_seguro.pdf]. (CRÍTICA)
- **Implementación:** Creación de GPO/Profiles → Aplicación por fases (Piloto → General).
- **Evidencias tri-SO:**
  | Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
  |---|---|---|---|---|
  | Cifrado | `Get-BitLockerVolume` [42-windows11_cis_benchmark.pdf] | `fdesetup status` [50-apple_platform_security.pdf] | `lsblk -o NAME,TYPE,FSTYPE \| grep crypt` / LUKS [87-debian-handbook.pdf] | Mensual |
  | Antimalware/EDR | `Get-MpComputerStatus` [82-windows-defender-evaluation-guide.pdf] | EDR process (`launchctl`) / XProtect status | Status daemon EDR (ej. `systemctl status falco/crowdstrike`) | Semanal |
  | Hardening SO | GPO Export / `gpresult` | MDM Configuration Profile export | `oscap xccdf eval` [84-article-openscap_en.pdf] o `ausearch` | Trimestral |
  | MAC / Sandboxing | AppLocker / WDAC configs | Gatekeeper status (`spctl --status`) | SELinux status / AppArmor status [110-sles-selinux_en.pdf] [83-apparmor201_sp10_admin.pdf] | Trimestral |

### D5. Red y Perímetro
- **Riesgo:** Interceptación, accesos perimetrales indebidos y ataques DDoS.
- **Recomendaciones:**
  - Firewalls de Nueva Generación (NGFW) con segmentación de sedes [33-proteccion_dos_cortafuegos.pdf]. (CRÍTICA)
  - Protección de Wi-Fi con WPA3/WPA2 Enterprise (802.1X) [35-seguridad_redes_wifi.pdf]. (ALTA)
- **Implementación:** Diseño VLANs → Reglas Deny-All by default → Despliegue.
- **Evidencias tri-SO:**
  | Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
  |---|---|---|---|---|
  | FW Local | `Get-NetFirewallProfile` | `socketfilterfw --getglobalstate` | `iptables -L` o `firewall-cmd --state` [78-red_hat_enterprise_linux-9-securing_networks-en-us.pdf] | Mensual |
  | 802.1x Network | Perfil WiFi EAP exportado | Perfil MDM Network/EAP-TLS | Config de `wpa_supplicant.conf` | Anual |

### D6. Vulnerabilidades y Parcheo
- **Riesgo:** Ejecución de exploits públicos (Zero-days / N-days).
- **Recomendaciones:**
  - Establecer SLAs de parcheo: Críticas < 7 días, Altas < 15 días, Medias < 30 días [05-ens_medidas_implantacion.pdf]. (CRÍTICA)
- **Implementación:** Escaneo semanal de credenciales → Remediation plan → Deploy.
- **Evidencias tri-SO:**
  | Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
  |---|---|---|---|---|
  | Patch Level | WSUS Reports / `Get-HotFix` | `softwareupdate --history` [73-managing_devices_and_corporate_data_on_ios.pdf]| Reportes `dnf updateinfo` / `apt list --upgradable` | Mensualmente |

### D7. Logging, Auditoría y Detección
- **Riesgo:** Incapacidad de investigar trazabilidad post-incidente.
- **Recomendaciones:**
  - Retención de logs locales de seguridad y reenvío a SIEM [16-principios_recomendaciones_basicas.pdf]. (ALTA)
- **Implementación:** Configurar Syslog/WEF → Configurar SIEM → Alertas de uso de root/Admin.
- **Evidencias tri-SO:**
  | Control | Evidencia Windows | Evidencia macOS | Evidencia Linux | Frecuencia |
  |---|---|---|---|---|
  | Log Forwarding | Windows Event Forwarding (WEF) configs [81-windows_event_logging_and_forwarding_october_2021.pdf] | `log show` daemon y profile config / Splunk UF | `rsyslog.conf` / `auditd` configs dirigidas a SIEM [74-ol8-auditing.pdf] | Continuo |

### D8. Backups, Continuidad y Recuperación
- **Riesgo:** Pérdida permanente de datos ante Ransomware o desastres físicos.
- **Recomendaciones:**
  - Estrategia 3-2-1 con copias offline o inmutables [57-copias_seguridad.pdf]. (CRÍTICA)
  - Pruebas semestrales de restauración. (ALTA)
- **Implementación:** Despliegue agente backup → Tareas automatizadas → Simulacros.
- **Evidencias:** Logs de finalización exitosa del software de backup, actas de simulacro de recuperación [11-pilar_impacto_continuidad.pdf].

### D9. Correo y Colaboración
- **Riesgo:** Spoofing, Phishing y Business Email Compromise (BEC).
- **Recomendaciones:**
  - DMARC en política `reject`, con SPF y DKIM habilitados [31-correo_dmarc.pdf]. (ALTA)
  - Filtrado de adjuntos y links maliciosos en entrada [30-correo_electronico_seguridad.pdf]. (CRÍTICA)
- **Implementación:** Check DNS → Activar firmas → Validar filtrado de red.
- **Evidencias:** Reportes DMARC (RUA/RUF), auditoría de cabeceras de correo recibido.

### D10. Seguridad Cloud (AWS, Azure)
- **Riesgo:** Desconfiguración (misconfiguration) exponiendo S3/Blob storage o VMs a internet.
- **Recomendaciones:**
  - Habilitar CSPM (Azure Defender para Cloud / AWS Security Hub) [99-azure-security-documentation.pdf] [96-aws_security_best_practices.pdf]. (CRÍTICA)
  - No exponer puertos de gestión directa a Internet (usar Bastion/SSM) [96-aws_security_best_practices.pdf]. (ALTA)
- **Implementación:** Revisión de Security Groups → Activación de logs (CloudTrail/Azure Monitor).
- **Evidencias:** Exportación de *Security Posture Score*, logs de CloudTrail.

### D11. AppSec / SDLC
- **Riesgo:** Despliegue de software con vulnerabilidades como inyecciones SQL o XSS.
- **Recomendaciones:**
  - Análisis SAST/DAST integrado en pipelines CI/CD [62-desarrollo_seguro.pdf]. (MEDIA/ALTA)
  - Dependabot o equivalente para escaneo de componentes terceros. (MEDIA)
  *(Nota: Si la empresa no desarrolla software a medida, este control aplica solo a la gestión de adquisiciones)*.
- **Implementación:** Configurar hooks de SonarQube / GitHub Advanced Security.
- **Evidencias:** Quality Gate reports en despliegues.

### D12. Respuesta a Incidentes
- **Riesgo:** Caos operativo ante incidentes aumenta el tiempo de inactividad de Días a Semanas.
- **Recomendaciones:**
  - Redactar y aprobar un Plan de Respuesta a Incidentes y Playbooks de Ransomware [20-gestion_crisis_incibe.pdf]. (CRÍTICA)
  - Realizar una prueba de escritorio (Tabletop) anual. (ALTA)
- **Implementación:** Documentar matriz de escalado → Contratar incident responder (retainer) → Ejercicios.
- **Evidencias:** Copia del Plan de R.I. actualizado, actas de Tabletop.

---

## 9. RGPD/LOPDGDD (Privacidad y Legal)

Esta sección cubre el cumplimiento del Reglamento General de Protección de Datos apoyado operativamente por TI.

- **Registro de Actividades de Tratamiento (ROPA):** Esencial mantener el inventario de flujos de datos [93-guia-rgpd-para-responsables-de-tratamiento.pdf].
- **Análisis de Riesgos y DPIA/EIPD:** Obligatorio previo a implementar nuevas tecnologías que profiling, biometría o datos masivos especiales (Art. 35 RGPD) [91-gestion-riesgo-y-evaluacion-impacto-en-tratamientos-datos-pe.pdf] [119-edpb-summary-gdpr-data-protection-design-default_en.pdf].
- **Gestión de Brechas de Personales:** Proceso para detectar y notificar a la AEPD en menos de 72 horas desde el conocimiento de la brecha [90-edpb_guidelines_202209_personal_data_breach_notification_v2.pdf] [92-guia-brechas-seguridad.pdf]. Se debe integrar este procedimiento con el SecOps (Dominio D12).
- **Encargados del Tratamiento:** Firma obligatoria de Data Processing Agreements (DPA) o Standard Contractual Clauses (SCC) si hay transferencias extra-comunitarias [138-si_sa_standard_contract_clauses_en.pdf] [129-lt_sa_standard_contractual_clauses_for_the_data_processing_a.pdf].
- **Anonimización y Minimización:** Aplicar seudonimización donde sea posible y borrar los registros cumplido su ciclo de retención legal [125-guia-orientaciones-procedimientos-anonimizacion.pdf].

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

"""

client_content = re.sub(r' \[[a-zA-Z0-9_\-\.]+?\.pdf\]', '', internal_content)
client_content = re.sub(r'\[[a-zA-Z0-9_\-\.]+?\.pdf\]', '', client_content)
client_content = client_content.replace('**Nivel:** Generalista (Adaptable a PYME y Gran Empresa)\n', '')
client_content = client_content.replace('*Version INTERNAL - Con trazabilidad al corpus*', '*Version CLIENTE - Executive Report*')
internal_content = internal_content.replace('**Nivel:**', '*Version INTERNAL - Con trazabilidad al corpus*\n**Nivel:**')

with open('deliverables/plan_seguridad_v2/INTERNAL.md', 'w') as f:
    f.write(internal_content)

with open('deliverables/plan_seguridad_v2/CLIENTE.md', 'w') as f:
    f.write(client_content)

print("Markdown documents generated.")
