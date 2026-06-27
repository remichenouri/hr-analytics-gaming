"""
Données spécifiques à l'industrie du gaming pour l'application Ubisoft
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class UbisoftSpecificData:
    """Données simulées spécifiques à Ubisoft et l'industrie gaming"""
    
    def __init__(self):
        self.ubisoft_studios = {
            'Paris': {'employees': 400, 'focus': 'R&D, Publishing'},
            'Montreal': {'employees': 4000, 'focus': 'AAA Development'},
            'Toronto': {'employees': 800, 'focus': 'Mobile, Live Services'},
            'Barcelona': {'employees': 300, 'focus': 'Mobile Games'},
            'Berlin': {'employees': 200, 'focus': 'Blue Byte Strategy'},
            'San Francisco': {'employees': 350, 'focus': 'Technology, AI'},
            'Kiev': {'employees': 600, 'focus': 'Development Support'}
        }
        
        self.gaming_roles = [
            'Game Developer', 'Game Designer', 'Technical Artist',
            'UI/UX Designer', 'Quality Assurance', 'Producer',
            'Community Manager', 'Data Analyst', 'DevOps Engineer',
            'Narrative Designer', '3D Artist', 'Animator',
            'Sound Designer', 'Marketing Specialist', 'HR Specialist'
        ]
        
        self.franchises = {
            'Assassins Creed': {
                'team_size': 800,
                'neurodiversity_correlation': 0.85,
                'creativity_score': 92
            },
            'Rainbow Six': {
                'team_size': 600,
                'neurodiversity_correlation': 0.78,
                'creativity_score': 88
            },
            'Far Cry': {
                'team_size': 450,
                'neurodiversity_correlation': 0.82,
                'creativity_score': 90
            },
            'Just Dance': {
                'team_size': 200,
                'neurodiversity_correlation': 0.76,
                'creativity_score': 85
            },
            'Watch Dogs': {
                'team_size': 350,
                'neurodiversity_correlation': 0.80,
                'creativity_score': 87
            }
        }
    
    def get_studio_demographics(self):
        """Génère les démographiques par studio"""
        data = []
        
        for studio, info in self.ubisoft_studios.items():
            # Simulation données démographiques
            for month in range(1, 13):
                data.append({
                    'Studio': studio,
                    'Month': month,
                    'Employees': info['employees'] + np.random.randint(-20, 50),
                    'Neurodivergent_Percentage': np.random.uniform(12, 22),
                    'Gender_Diversity': np.random.uniform(0.3, 0.5),  # Pourcentage femmes
                    'Age_Average': np.random.uniform(28, 35),
                    'Satisfaction_Score': np.random.uniform(3.8, 4.5),
                    'Innovation_Rating': np.random.uniform(75, 95),
                    'Focus_Area': info['focus']
                })
        
        return pd.DataFrame(data)
    
    def get_franchise_performance(self):
        """Données de performance par franchise"""
        data = []
        
        for franchise, metrics in self.franchises.items():
            # Données trimestrielles
            for quarter in range(1, 5):
                base_creativity = metrics['creativity_score']
                neurodiv_impact = metrics['neurodiversity_correlation']
                
                data.append({
                    'Franchise': franchise,
                    'Quarter': f'Q{quarter} 2024',
                    'Team_Size': metrics['team_size'] + np.random.randint(-50, 100),
                    'Creativity_Score': base_creativity + np.random.uniform(-5, 5),
                    'Innovation_Index': base_creativity * neurodiv_impact + np.random.uniform(-10, 10),
                    'User_Rating': np.random.uniform(7.5, 9.2),
                    'Revenue_Impact': np.random.uniform(50, 200),  # Millions €
                    'Neurodiversity_Level': np.random.uniform(15, 25),
                    'Problem_Solving_Score': np.random.uniform(80, 95),
                    'Collaboration_Rating': np.random.uniform(85, 98)
                })
        
        return pd.DataFrame(data)
    
    def get_industry_benchmarks(self):
        """Benchmarks industrie gaming"""
        companies = [
            'Ubisoft', 'Electronic Arts', 'Activision Blizzard', 
            'Riot Games', 'Epic Games', 'CD Projekt', 'Bungie'
        ]
        
        data = []
        
        for company in companies:
            # Ubisoft légèrement avantagé dans certaines métriques
            if company == 'Ubisoft':
                turnover = np.random.uniform(10, 15)
                satisfaction = np.random.uniform(4.0, 4.4)
                diversity = np.random.uniform(0.68, 0.75)
                innovation = np.random.uniform(85, 95)
            else:
                turnover = np.random.uniform(15, 25)
                satisfaction = np.random.uniform(3.5, 4.1)
                diversity = np.random.uniform(0.55, 0.70)
                innovation = np.random.uniform(70, 90)
            
            data.append({
                'Company': company,
                'Annual_Turnover_Rate': turnover,
                'Employee_Satisfaction': satisfaction,
                'Diversity_Index': diversity,
                'Innovation_Score': innovation,
                'Revenue_Billions': np.random.uniform(1.5, 8.5),
                'Employee_Count': np.random.randint(2000, 20000),
                'Neurodiversity_Programs': np.random.choice([0, 1], p=[0.7, 0.3]),
                'Remote_Work_Policy': np.random.uniform(0.3, 0.8)
            })
        
        return pd.DataFrame(data)
    
    def get_skill_demand_trends(self):
        """Tendances demande de compétences gaming"""
        skills = [
            'Unity Development', 'Unreal Engine', 'Data Analytics',
            'AI/Machine Learning', 'Cloud Gaming', 'AR/VR Development',
            'Neurodiversity Awareness', 'UX Research', 'DevOps',
            'Community Management', 'Live Operations', 'Monetization'
        ]
        
        data = []
        
        # Données sur 2 ans
        months = pd.date_range(start='2023-01-01', periods=24, freq='M')
        
        for skill in skills:
            for month in months:
                # Neurodiversity Awareness en forte croissance
                if 'Neurodiversity' in skill:
                    demand = 20 + (month.month * 2) + np.random.uniform(-5, 10)
                else:
                    demand = np.random.uniform(40, 90)
                
                data.append({
                    'Skill': skill,
                    'Month': month,
                    'Demand_Score': min(100, max(0, demand)),
                    'Salary_Premium': np.random.uniform(0, 25),  # % bonus
                    'Ubisoft_Priority': np.random.choice([1, 2, 3, 4, 5]),
                    'Market_Availability': np.random.uniform(20, 80)
                })
        
        return pd.DataFrame(data)

# Fonctions utilitaires pour les données gaming
def get_gaming_industry_stats():
    """Statistiques clés industrie gaming"""
    return {
        'global_revenue_2024': '184.4 Billion USD',
        'gaming_workforce_growth': '8.2% annually',
        'neurodivergent_population': '15-20% (estimated)',
        'remote_work_adoption': '67% post-COVID',
        'ai_adoption_rate': '45% of studios',
        'diversity_investment': '2.3 Billion USD (2023-2024)'
    }

def calculate_gaming_roi_multipliers():
    """Multiplicateurs ROI spécifiques gaming"""
    return {
        'creativity_boost': 1.8,
        'innovation_premium': 2.2,
        'retention_value': 1.5,
        'neurodiversity_multiplier': 1.25,
        'franchise_value_impact': 3.5,
        'user_engagement_correlation': 0.73
    }
