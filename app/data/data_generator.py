import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class GamingIndustryDataGenerator:
    def __init__(self):
        self.companies = ['Ubisoft', 'EA', 'Activision', 'Riot Games', 'Blizzard']
        self.studios = {
            'Ubisoft': ['Paris', 'Montreal', 'Toronto', 'Barcelona', 'Berlin'],
            'EA': ['Redwood City', 'Vancouver', 'Austin', 'Guildford', 'Stockholm'],
            'Activision': ['Santa Monica', 'Austin', 'Shanghai', 'London', 'Warsaw']
        }
        
    def generate_workforce_data(self):
        """Génère les données de workforce pour comparaison"""
        data = []
        
        for company in self.companies:
            # Données Ubisoft (vos cibles) plus favorables
            if company == 'Ubisoft':
                turnover_rate = np.random.normal(12, 2, 12)  # Taux plus bas
                satisfaction = np.random.normal(4.2, 0.3, 12)  # Satisfaction plus haute
                diversity_score = np.random.normal(0.72, 0.05, 12)  # Meilleur D&I
            else:
                turnover_rate = np.random.normal(18, 3, 12)
                satisfaction = np.random.normal(3.8, 0.4, 12)
                diversity_score = np.random.normal(0.65, 0.08, 12)
            
            for month in range(12):
                data.append({
                    'Company': company,
                    'Month': month + 1,
                    'Turnover_Rate': max(5, min(30, turnover_rate[month])),
                    'Employee_Satisfaction': max(1, min(5, satisfaction[month])),
                    'Diversity_Score': max(0.4, min(1.0, diversity_score[month])),
                    'Headcount': np.random.randint(800, 1500) if company == 'Ubisoft' else np.random.randint(600, 2000)
                })
        
        return pd.DataFrame(data)
    
    def generate_neurodiversity_data(self):
        """Génère les données sur l'impact de la neurodiversité"""
        data = []
        
        # Simulation corrélation neurodiversité/innovation
        neurodiversity_levels = np.arange(0.05, 0.25, 0.01)  # 5% à 25%
        
        for level in neurodiversity_levels:
            # Plus de neurodiversité = plus d'innovation (votre hypothèse)
            innovation_score = 60 + (level * 100 * 0.8) + np.random.normal(0, 5)
            creativity_index = 0.6 + (level * 1.5) + np.random.normal(0, 0.1)
            problem_solving = 70 + (level * 80) + np.random.normal(0, 8)
            
            data.append({
                'Neurodiversity_Percentage': level * 100,
                'Innovation_Score': max(50, min(100, innovation_score)),
                'Creativity_Index': max(0.3, min(1.5, creativity_index)),
                'Problem_Solving_Score': max(60, min(100, problem_solving)),
                'Team_Performance': max(65, min(95, 70 + level * 120 + np.random.normal(0, 6)))
            })
        
        return pd.DataFrame(data)
    
    def generate_retention_data(self):
        """Génère les données pour les modèles de rétention"""
        np.random.seed(42)  # Pour reproductibilité
        n_employees = 1000
        
        data = []
        for i in range(n_employees):
            # Facteurs influençant la rétention
            salary_percentile = np.random.uniform(20, 95)
            work_life_balance = np.random.uniform(1, 5)
            career_growth = np.random.uniform(1, 5)
            manager_quality = np.random.uniform(1, 5)
            neurodivergent = np.random.choice([0, 1], p=[0.85, 0.15])
            
            # Modèle de rétention (logique simplifiée)
            retention_score = (
                salary_percentile * 0.3 +
                work_life_balance * 15 +
                career_growth * 20 +
                manager_quality * 18 +
                neurodivergent * 25 +  # Bonus neurodiversité
                np.random.normal(0, 10)
            )
            
            stayed = 1 if retention_score > 70 else 0
            
            data.append({
                'Employee_ID': f'EMP_{i:04d}',
                'Salary_Percentile': salary_percentile,
                'Work_Life_Balance': work_life_balance,
                'Career_Growth': career_growth,
                'Manager_Quality': manager_quality,
                'Is_Neurodivergent': neurodivergent,
                'Retention_Score': max(0, min(100, retention_score)),
                'Stayed': stayed,
                'Department': np.random.choice(['Game Dev', 'Art', 'QA', 'Marketing', 'HR'])
            })
        
        return pd.DataFrame(data)
    
    def generate_roi_data(self):
        """Génère les données pour le calculateur ROI"""
        programs = [
            'Neurodiversity Hiring Initiative',
            'Flexible Work Arrangements', 
            'Manager Training Program',
            'Employee Resource Groups',
            'Mental Health Support',
            'Inclusive Design Workshops'
        ]
        
        data = []
        for program in programs:
            # Coûts et bénéfices simulés
            implementation_cost = np.random.uniform(50000, 200000)
            annual_cost = np.random.uniform(20000, 100000)
            
            # Bénéfices (plus importants pour neurodiversity programs)
            if 'neurodiversity' in program.lower():
                retention_improvement = np.random.uniform(25, 35)
                productivity_gain = np.random.uniform(18, 28)
                innovation_boost = np.random.uniform(20, 30)
            else:
                retention_improvement = np.random.uniform(10, 20)
                productivity_gain = np.random.uniform(8, 15)
                innovation_boost = np.random.uniform(5, 15)
            
            data.append({
                'Program': program,
                'Implementation_Cost': implementation_cost,
                'Annual_Cost': annual_cost,
                'Retention_Improvement_Percent': retention_improvement,
                'Productivity_Gain_Percent': productivity_gain,
                'Innovation_Boost_Percent': innovation_boost,
                'Employee_Satisfaction_Increase': np.random.uniform(0.3, 0.8)
            })
        
        return pd.DataFrame(data)
