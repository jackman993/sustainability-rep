"""Environment 引擎模組"""

from .environment_pptx import EnvironmentPPTXEngine


def generate_environment_pptx_for_streamlit(
    *,
    api_key: str | None,
    industry: str,
    emission_data: dict | None = None,
    tcfd_output_folder: str | None = None,
    emission_output_folder: str | None = None,
    company_profile: dict | None = None,
    test_mode: bool = False,
):
    """
    專給 Streamlit Step2 使用的入口函式。
    - 使用 EnvironmentPPTXEngine 生成完整 Chapter 4 PPTX
    - 內部不處理檔案儲存，只回傳 Presentation 物件，由上層決定存到哪裡
    """
    emission_data = emission_data or {}
    company_profile = company_profile or {}

    engine = EnvironmentPPTXEngine(
        template_path=None,  # 使用預設 assets/handdrawppt.pptx
        test_mode=test_mode,
        emission_data=emission_data,
        industry=industry,
        tcfd_output_folder=tcfd_output_folder,
        emission_output_folder=emission_output_folder,
        company_profile=company_profile,
        api_key=api_key,
    )
    prs = engine.generate()
    return prs

