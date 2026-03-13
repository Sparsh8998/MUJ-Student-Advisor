# 🎓 MUJ Student Advisor AI
### PS 01: Student Academic Performance Prediction & Personalized Intervention
**Developed for IEEE CIS AI Model Quest 2.0**

The **MUJ Student Advisor AI** is a proactive, data-driven institutional tool designed to transform academic advising from a reactive process into a predictive science. By analyzing 15 distinct factors across academic, psychological, and environmental domains, this system identifies at-risk students weeks before examinations and provides automated, personalized recovery plans.

---

## 🎯 Key Features
* **Predictive Analysis:** Real-time grade tier classification using a high-accuracy Random Forest Ensemble model.
* **Confidence Meter:** Visualizes the statistical probability distribution behind every AI prediction to provide transparency in decision-making.
* **Institutional Intervention:** Generates hyper-personalized Success Plans based on official university guidelines for each risk level.
* **Comparative Dashboard:** Benchmarks individual student metrics against campus performance averages to highlight specific areas for improvement.
* **Demo Profiles:** One-click loading of sample student profiles to instantly showcase the system's predictive capabilities.

---

## 🛠️ Technical Model Approach
The system employs a **Random Forest Ensemble** modeling strategy to ensure institutional-grade reliability.

### 1. Algorithm Selection
* **Ensemble Power:** By merging multiple decision trees, the model ensures stable predictions and effectively prevents the overfitting common in simpler algorithms.
* **Handling Non-Linearity:** The algorithm captures complex interactions between "hidden factors," such as how high stress levels impact study hours differently depending on motivation.

### 2. Feature Breadth (The 15 Predictors)
The model processes a 360-degree student profile including:
* **Academic:** Study Hours, Attendance %, Assignment Completion, and Exam Scores.
* **Psychological:** Motivation Level, Stress Level, and preferred Learning Style.
* **Environmental:** Internet Access, Resource Quality, and Educational Tech usage.
* **Social:** Extracurricular participation and Academic Discussion engagement.

### 3. Training & Performance
* **Data Preparation:** The dataset was split into 80% Training and 20% Testing sets using **Stratified Sampling** to maintain proportional grade category representation.
* **Reliability:** The model achieved a **99.0% accuracy** rate on test and validation datasets.

---

## 🚀 How to Run Locally

Follow these steps to set up and run the advisor system on your machine:

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your system.

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/muj-student-advisor.git](https://github.com/YOUR_GITHUB_USERNAME/muj-student-advisor.git)
cd muj-student-advisor
