"""
ESG Environment Chapter Report Generator - Configuration File
"""
import os

# API Settings
ANTHROPIC_API_KEY = "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"
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Using Claude Sonnet 4 (consistent with TCFD Generator)

# Path Settings (using absolute paths to ensure correct cross-directory calls)
import pathlib
ASSETS_PATH = str(pathlib.Path(__file__).parent / "assets")

# Environment Chapter Basic Configuration
ENVIRONMENT_CONFIG = {
    'chapter_title': 'Chapter 4 Environmental Sustainability',
    'total_pages': 17,
    'layout': '16:9',  # Changed to 16:9 aspect ratio
    'font_family': 'Microsoft JhengHei',
    'font_size': 10,  # Small font
    'table_split': '50_50'  # 50% left and right
}

# Detailed Configuration for Each Page
PAGE_CONFIGS = {
    'cover': {
        'layout': 'left_image_right_text',
        'title': 'Chapter 4 Environmental Sustainability',
        'image': 'picture4-0Environment_cover.png',
        'content_method': 'generate_environmental_cover',
        'word_count': 250
    },
    'page_1': {
        'layout': 'left_image_right_text',
        'title': '4.1 Environmental Policy and Management Framework',
        'image': 'picture4-1sustainability_penal.png',
        'content_method': 'generate_sustainability_committee',
        'word_count': 250
        
    },
    'page_2': {
        'layout': 'left_text_right_image',
        'title': '4.2 Four Dimensions of Environmental Policy',
        'image': 'picture4-2policy.png',
        'content_method': 'generate_policy_description',
        'word_count': 250

    },
    'page_3': {
        'layout': 'single_table',
        'title': 'TCFD Transition Risk',
        'table_file': 'tcfd_table_01_transformation_risk.py'
    },
    'page_4': {
        'layout': 'single_table',
        'title': 'TCFD Market Risk',
        'table_file': 'tcfd_table_02_market_risk.py'
    },
    'page_5': {
        'layout': 'single_table',
        'title': 'TCFD Physical Risk',
        'table_file': 'tcfd_table_03_physical_risk.py'
    },
    'page_6': {
        'layout': 'single_table',
        'title': 'TCFD Temperature Rise Risk',
        'table_file': 'tcfd_table_04_temperature_rise.py'
    },
    'page_7': {
        'layout': 'single_table',
        'title': 'TCFD Resource Efficiency Opportunities',
        'table_file': 'tcfd_table_05_resource_efficiency.py'
    },
    'page_8': {
        'layout': 'single_table',
        'title': 'TCFD Main Framework Description',
        'table_file': 'TCFD_main.py'
    },
    'page_9': {
        'layout': 'left_text_right_image',
        'title': 'TCFD Risk Matrix Analysis',
        'image': 'picture4-3TCFD_matrix.png',
        'content_method': 'generate_tcfd_matrix_analysis',
        'word_count': 250
    },
    'page_10': {
        'layout': 'left_table_right_text',
        'title': '4.5 Greenhouse Gas Emission Management',
        'table_file': 'emission_table.py',
        'content_method': 'generate_ghg_calculation_method',
        'word_count': 250
    },
    'page_11': {
        'layout': 'left_image_right_text',
        'title': 'Electricity Usage and Energy Conservation Policy',
        'image': 'picture4-4ghg_pie_scope.png',
        'content_method': 'generate_electricity_policy',
        'word_count': 250
    },
    'page_12': {
        'layout': 'left_text_right_image',
        'title': 'Energy Efficiency Measures',
        'image': 'picture4-5ghg_bar.png',
        'content_method': 'generate_energy_efficiency_measures',
        'word_count': 250
    },
    'page_13': {
        'layout': 'left_image_right_text',
        'title': '4.6 Green Planting',
        'image': 'picture4-6plant.png',
        'content_method': 'generate_green_planting_program',
        'word_count': 250
    },
    'page_14': {
        'layout': 'left_text_right_image',
        'title': '4.7 Water Resource Management',
        'image': 'picture4-7water.png',
        'content_method': 'generate_water_management',
        'word_count': 250

    },
    'page_15': {
        'layout': 'left_text_right_image',
        'title': '4.8 Waste Management',
        'image': 'picture4-8waste.png',
        'content_method': 'generate_waste_management',
        'word_count': 250
    },
    'page_16': {
        'layout': 'left_text_right_image',
        'title': '4.9 Environmental Education and Cooperation',
        'image': 'picture4-9ecowork.png',
        'content_method': 'generate_environmental_education',
        'word_count': 250
    }
}

# Page Order
PAGE_ORDER = ['cover', 'page_1', 'page_2', 'page_3', 'page_4', 'page_5', 'page_6', 
              'page_7', 'page_8', 'page_9', 'page_10', 'page_11', 'page_12', 
              'page_13', 'page_14', 'page_15', 'page_16']

# Image Mapping (all images are in assets folder)
ENVIRONMENT_IMAGE_MAPPING = {
    'cover': 'picture4-0Environment_cover.png',  # Updated: now .png format
    'sustainability_panel': 'picture4-1sustainability_penal.png',
    'policy': 'picture4-2policy.png',
    'tcfd_matrix': 'picture4-3TCFD_matrix.png',
    'ghg_pie': 'picture4-4ghg_pie_scope.png',
    'ghg_bar': 'picture4-5ghg_bar.png',
    'plant': 'picture4-6plant.png',  # Updated: now .png format
    'water': 'picture4-7water.png',
    'waste': 'picture4-8waste.png',
    'ecowork': 'picture4-9ecowork.png'
}

# TCFD Table Mapping (all .py files are in assets folder)
TCFD_TABLES = {
    'transformation_risk': 'tcfd_table_01_transformation_risk.py',
    'market_risk': 'tcfd_table_02_market_risk.py',
    'physical_risk': 'tcfd_table_03_physical_risk.py',
    'temperature_rise': 'tcfd_table_04_temperature_rise.py',
    'resource_efficiency': 'tcfd_table_05_resource_efficiency.py',
    'main_framework': 'TCFD_main.py'
}