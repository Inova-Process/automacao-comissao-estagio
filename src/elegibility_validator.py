import numpy as np
import pandas as pd

from boa_scraper import analyze_course_completion


def validate_company_affiliation(companies_df: pd.DataFrame, company_name: str) -> bool:
    # Maybe we should validate the company`s CNPJ instead of the name?
    institutions = companies_df["INSTITUIÇÃO"].values
    index = np.searchsorted(institutions, company_name)

    if not (index < len(institutions) and institutions[index] == company_name):
        return False

    return True


def requires_extension_hours(ano_ingresso) -> bool:
    """Retorna True quando as horas de extensão são obrigatórias para o aluno."""
    try:
        ano, semestre = str(ano_ingresso).split(".")
        return (int(ano), int(semestre)) >= (25, 1)
    except (ValueError, TypeError):
        # Se não for possível identificar o período de ingresso,
        # mantém a exigência por segurança.
        return True


def validate_eligibility(
    academic_data: dict,
    companies_df: pd.DataFrame,
    boa_path: str
) -> dict:

    academic_requirements = {
        "minimum_cr": 6.0,
        "max_periods": academic_data["prazo_maximo"],
        "minimum_ext_hours": 160.0,
        "minimum_credits": 87
    }

    exige_extensao = requires_extension_hours(academic_data.get("ano_ingresso"))

    validations_dict = {
        "valid_cr": True,
        "valid_periods": True,
        "valid_ext_hours": True,
        "valid_company": True,
        "valid_credits": True,
        "valid_courses": True,
        "valid_student": True,
        "requires_ext_hours": exige_extensao
    }

    # Validação do CR
    if academic_data["cr_acumulado"] < academic_requirements["minimum_cr"]:
        validations_dict["valid_cr"] = False
        validations_dict["valid_student"] = False

    # Validação do prazo de integralização
    if academic_data["periodos_integralizados"] > academic_requirements["max_periods"]:
        validations_dict["valid_periods"] = False
        validations_dict["valid_student"] = False

    # Validação das horas de extensão
    if (
        exige_extensao
        and academic_data["carga_horaria_extensao"] < academic_requirements["minimum_ext_hours"]
    ):
        validations_dict["valid_ext_hours"] = False
        validations_dict["valid_student"] = False

    # Validação da empresa será utilizada futuramente
    # if not validate_company_affiliation(companies_df, company_name):
    #     validations_dict["valid_company"] = False
    #     validations_dict["valid_student"] = False

    report = analyze_course_completion(boa_path)
    validations_dict["report"] = report

    # Validação dos créditos
    if academic_data["creditos_obtidos"] < academic_requirements["minimum_credits"]:
        validations_dict["valid_credits"] = False
        validations_dict["valid_courses"] = False
        validations_dict["valid_student"] = False
        return validations_dict

    # Validação das disciplinas obrigatórias
    if not report["status"]["cumpriu_todas_materias"]:
        validations_dict["valid_courses"] = False
        validations_dict["valid_student"] = False

    return validations_dict