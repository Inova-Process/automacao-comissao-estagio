import streamlit as st


def report_card(academic_data, validations_dict):
    """
    Gera um card de relatório de elegibilidade no Streamlit.

    Args:
        validations_dict (dict): Dicionário com os resultados booleanos das validações.
        academic_data (dict): Dicionário com os dados acadêmicos do estudante.
    """

    # --- Container Principal para o Card ---
    with st.container(border=True):
        st.subheader(
            f"Resultado para {academic_data.get('nome_aluno', 'Aluno Desconhecido')}"
        )
        st.markdown("---")

        # --- Status Final (APTO/INAPTO) ---
        if validations_dict.get("valid_student", False):
            st.success("✅ PARABÉNS! O(A) aluno(a) está APTO(A).")
        else:
            st.error("❌ ATENÇÃO! O(A) aluno(a) está INAPTO(A).")

        st.write("")

        # --- Painel de Desempenho Rápido ---
        st.write("**Painel de Desempenho**")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="CR Acumulado",
                value=f'{academic_data.get("cr_acumulado", 0.0)}'
            )

        with col2:
            periodos = academic_data.get("periodos_integralizados", 0)
            prazo_maximo = academic_data.get("prazo_maximo", 0)

            st.metric(
                label="Períodos Integralizados",
                value=f"{periodos:g} / {prazo_maximo:g}"
            )

        with col3:
            st.metric(
                label="Horas de Extensão",
                value=f'{academic_data.get("carga_horaria_extensao", 0)}h'
            )

        st.write("")

        # --- Expander para Detalhes dos Critérios ---
        with st.expander("Ver análise detalhada dos critérios"):

            academic_requirements = {
                "minimum_cr": 6.0,
                "max_periods": academic_data["prazo_maximo"],
                "minimum_ext_hours": 160.0,
                "minimum_credits": 87
            }

            criteria_map = {
                "valid_cr": {
                    "name": "Coeficiente de Rendimento",
                    "value": academic_data.get("cr_acumulado"),
                    "required": academic_requirements["minimum_cr"]
                },

                "valid_periods": {
                    "name": "Períodos Integralizados",
                    "value": academic_data.get("periodos_integralizados"),
                    "required": f'<= {academic_requirements["max_periods"]}'
                },

                "valid_ext_hours": {
                    "name": "Horas de Extensão",
                    "value": academic_data.get("carga_horaria_extensao"),
                    "required": f">= {academic_requirements['minimum_ext_hours']}"
                },

                # "valid_company": {
                #     "name": "Empresa Conveniada",
                #     "value": validations_dict.get("valid_company"),
                #     "required": "True"
                # },

                "valid_courses": {
                    "name": "Disciplinas Obrigatórias",
                    "value": validations_dict.get("valid_courses"),
                    "required": "True"
                },
            }

            for key, validation_status in validations_dict.items():
                if key in criteria_map:
                    details = criteria_map[key]
                    icon = "✅" if validation_status else "❌"

                    st.markdown(
                        f"{icon} **{details['name']}**"
                    )

                    # Adiciona a explicação se o critério não foi cumprido
                    if not validation_status:

                        if key == "valid_cr":
                            st.markdown(
                                f"**Por que?** Seu Coeficiente de Rendimento (CR) "
                                f"está abaixo do mínimo exigido. Para ser elegível, "
                                f"o aluno deve manter um CR de "
                                f"`{academic_requirements['minimum_cr']}` ou superior. "
                                f"Seu CR atual é de "
                                f"`{academic_data.get('cr_acumulado')}`."
                            )

                            st.markdown(
                                "**Como resolver?** Entre em contato com a COAA ou "
                                "com seu orientador acadêmico para discutir estratégias "
                                "de melhoria acadêmica, como monitorias, grupos de estudo "
                                "ou aconselhamento acadêmico."
                            )

                        elif key == "valid_periods":
                            st.markdown(
                                f"**Por que?** O aluno excedeu o número máximo de "
                                f"períodos para a conclusão do curso. O prazo máximo é de "
                                f"`{academic_requirements['max_periods']}` períodos e o "
                                f"aluno já integralizou "
                                f"`{academic_data.get('periodos_integralizados')}`."
                            )

                            st.markdown(
                                "**Como resolver?** Entre em contato com a COAA ou "
                                "com seu orientador acadêmico para analisar o seu caso."
                            )

                        elif key == "valid_ext_hours":
                            ano_ingresso = academic_data.get("ano_ingresso", "")

                            if int(ano_ingresso[0:2]) < 25:
                                st.info(
                                    "ℹ️ **Recomendação (Horas de Extensão):** \n\n"
                                    "Notamos que você ingressou antes de 25.1. "
                                    "Para a sua grade curricular, as horas de extensão "
                                    "**não são um requisito obrigatório** para a validação "
                                    "do estágio, mas são **altamente recomendadas** para "
                                    "uma experiência acadêmica mais completa."
                                )

                            else:
                                st.markdown(
                                    f"**Por que?** A carga horária de extensão registrada "
                                    f"está abaixo do requisito mínimo. O aluno precisa "
                                    f"completar um total de "
                                    f"`{academic_requirements['minimum_ext_hours']}` horas "
                                    f"de extensão, mas a carga horária atual é de "
                                    f"`{academic_data.get('carga_horaria_extensao')}` horas."
                                )

                                st.markdown(
                                    "**Como resolver?** Considere participar de atividades "
                                    "de extensão oferecidas pela universidade. Confira as "
                                    "opções disponíveis em: "
                                    "https://portal.ufrj.br/Registro/requerimento/aluno/extensao/filtro"
                                )

                        elif key == "valid_courses":
                            st.markdown(
                                "**Por que?** O aluno ainda não foi aprovado em todas "
                                "as disciplinas obrigatórias necessárias para o programa. "
                                "É essencial que todas as matérias obrigatórias até o "
                                "quarto período sejam concluídas."
                            )

                            materias_pendentes = (
                                validations_dict
                                .get("report", {})
                                .get("status", {})
                                .get("materias_pendentes")
                            )

                            if materias_pendentes:
                                expander_label = (
                                    f"Matérias Pendentes "
                                    f"({len(materias_pendentes)})"
                                )

                                with st.expander(expander_label):
                                    nomes_materias = (
                                        validations_dict
                                        .get("report", {})
                                        .get("nomes_materias", {})
                                    )

                                    for materia in materias_pendentes:
                                        nome = nomes_materias.get(materia)

                                        if nome:
                                            st.markdown(
                                                f"- **{materia}** — {nome}"
                                            )
                                        else:
                                            st.markdown(
                                                f"- **{materia}**"
                                            )

                            else:
                                st.caption(
                                    "Não há matérias pendentes para exibir."
                                )

                        st.markdown("")