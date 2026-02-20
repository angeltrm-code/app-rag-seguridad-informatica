# Reporte de Duplicados — 2026-02-20 13:31

## Resumen

| Métrica | Valor |
|---------|-------|
| PDFs analizados | 94 |
| Duplicados exactos (vs corpus) | 5 |
| Duplicados internos (dentro del lote) | 18 |
| Near-duplicates (flagged) | 3 |
| Aceptados (nuevos) | 71 |

## Duplicados Exactos (hash SHA-256)

| Archivo Incoming | Existente en Corpus | Hash |
|-----------------|--------------------|---------|
| `NIST.CSWP.29.pdf` | `07-nist_csf_v2.pdf` | `3c31f46fee98cac0…` |
| `apple-platform-security-guide.pdf` | `50-apple_platform_security.pdf` | `46702ba1467717fc…` |
| `guia_gestion_de_crisis.pdf` | `20-gestion_crisis_incibe.pdf` | `5386b8e1db1dabbc…` |
| `macos__apple-platform-security-guide.pdf` | `50-apple_platform_security.pdf` | `46702ba1467717fc…` |
| `rgpd_lopd__ciberseguridad_en_el_teletrabajo.pdf` | `67-teletrabajo_incibe.pdf` | `73c0d58d1bb5cb55…` |

**Decisión:** SKIPPED — movidos a `_skipped_duplicates/`

## Duplicados Internos (dentro del lote)

| Archivo | Duplicado de | Hash |
|---------|-------------|------|
| `Red_Hat_Enterprise_linux-9-Security_hardening-en-US.pdf` | `Red_Hat_Enterprise_Linux-9-Security_hardening-en-US.pdf` | `1852d18da039b122…` |
| `linux__6-best-practices-for-amazon-security-groups__710697a5.pdf` | `linux__6-best-practices-for-amazon-security-groups.pdf` | `190abc9b6c7773bd…` |
| `linux__Red_Hat_Enterprise_Linux-9-Security_hardening-en-US.pdf` | `Red_Hat_Enterprise_Linux-9-Security_hardening-en-US.pdf` | `1852d18da039b122…` |
| `linux__book-security_en.pdf` | `book-security_en.pdf` | `fd905c3977bed9cd…` |
| `linux_extra__OL8-AUDITING.pdf` | `OL8-AUDITING.pdf` | `06f2a8262655cdfe…` |
| `linux_extra__Red_Hat_Enterprise_Linux-9-Securing_networks-en-US.pdf` | `Red_Hat_Enterprise_linux-9-Securing_networks-en-US.pdf` | `aca6204be690dba4…` |
| `linux_extra__Red_Hat_Enterprise_linux-9-Security_hardening-en-US.pdf` | `Red_Hat_Enterprise_Linux-9-Security_hardening-en-US.pdf` | `1852d18da039b122…` |
| `linux_extra__The-SELinux_Notebook-Volume-1-The-Foundations.pdf` | `The-SELinux=Notebook-Volume-1-The-Foundations.pdf` | `f45ba5d34417f872…` |
| `linux_extra__apparmor201_sp10_admin.pdf` | `apparmor201_sp10_admin.pdf` | `4b7d6600e86fcc42…` |
| `linux_extra__article-openscap_en.pdf` | `article-openscap_en.pdf` | `121eb16d0e2612ea…` |
| `linux_extra__book-administration_en.pdf` | `book-administration_en.pdf` | `660bf0d598f79d5e…` |
| `linux_extra__debian-handbook.pdf` | `debian-handbook.pdf` | `b9d48e185829f9ed…` |
| `nistspecialpublication800-123.pdf` | `linux__nistspecialpublication800-123.pdf` | `182ae5d23011108f…` |
| `rgpd_lopd__edpb_guidelines_201904_dataprotection_by_design_and_by_default_v2.0_en.pdf` | `edpb_guidelines_201904_dataprotection_by_design_and_by_default_v2.0_en.pdf` | `179c669a3aac9a2c…` |
| `rgpd_lopd__guia-rgpd-para-responsables-de-tratamiento.pdf` | `guia-rgpd-para-responsables-de-tratamiento.pdf` | `2011744c636364d4…` |
| `rgpd_lopd__guia_nacional_notificacion_gestion_ciberincidentes.pdf` | `guia_nacional_notificacion_gestion_ciberincidentes.pdf` | `9a2ef654d3079916…` |
| `securing-debian-manual.en.pdf` | `linux__securing-debian-manual.en.pdf` | `04b48f72e7851f8b…` |
| `security-hardening.pdf` | `linux_extra__security-hardening.pdf` | `1cde1984e88f0c2e…` |

**Decisión:** SKIPPED — movidos a `_skipped_duplicates/`

## Near-Duplicates (similitud de nombre)

| Archivo | Nota |
|---------|------|
| `guia-brechas-seguridad.pdf` | 72% similar to 68-kubernetes_seguridad.pdf |
| `macos__apple-platform-security-guide-b.pdf` | 88% similar to 50-apple_platform_security.pdf |
| `rgpd_lopd__metad_plan-director-seguridad.pdf` | 89% similar to 15-plan_director_seguridad.pdf |

**Decisión:** ACCEPTED — incluidos pero marcados para revisión manual

