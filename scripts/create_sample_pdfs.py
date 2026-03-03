"""
Create sample medical knowledge base PDFs from public health information.
Uses general medical knowledge that is publicly available.
"""

from fpdf import FPDF
from pathlib import Path

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge_base"
KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)


def create_pdf(filename: str, title: str, sections: list[tuple[str, str]]):
    """Create a formatted PDF with title and sections."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 15, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 8, "Public Health Information Guide", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)

    for heading, body in sections:
        # Section heading
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, heading, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Section body
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, body)
        pdf.ln(5)

    pdf.output(str(KNOWLEDGE_BASE_DIR / filename))
    print(f"Created: {filename}")


# --- PDF 1: Diabetes Overview ---
create_pdf("Diabetes-Overview.pdf", "Understanding Diabetes", [
    ("What is Diabetes?",
     "Diabetes is a chronic metabolic disease characterized by elevated levels of blood glucose (blood sugar), which over time leads to serious damage to the heart, blood vessels, eyes, kidneys, and nerves. The most common type is Type 2 diabetes, which occurs when the body becomes resistant to insulin or does not produce enough insulin. Type 1 diabetes is an autoimmune condition where the pancreas produces little or no insulin."),

    ("Types of Diabetes",
     "Type 1 Diabetes: An autoimmune condition where the immune system attacks insulin-producing beta cells in the pancreas. It is usually diagnosed in children and young adults. Patients require daily insulin injections.\n\n"
     "Type 2 Diabetes: The most common form, accounting for about 90-95% of all diabetes cases. The body does not use insulin properly (insulin resistance). It is often associated with obesity, physical inactivity, and family history.\n\n"
     "Gestational Diabetes: Develops during pregnancy and usually resolves after delivery. However, it increases the risk of developing Type 2 diabetes later in life."),

    ("Symptoms",
     "Common symptoms of diabetes include:\n"
     "- Increased thirst and frequent urination\n"
     "- Unexplained weight loss\n"
     "- Extreme fatigue\n"
     "- Blurred vision\n"
     "- Slow-healing sores or frequent infections\n"
     "- Tingling or numbness in hands or feet\n"
     "- Areas of darkened skin (acanthosis nigricans)\n\n"
     "Type 1 symptoms can develop quickly over weeks. Type 2 symptoms often develop slowly over years and may go unnoticed."),

    ("Risk Factors for Type 2 Diabetes",
     "Several factors increase the risk of developing Type 2 diabetes:\n"
     "- Being overweight or obese (BMI over 25)\n"
     "- Age 45 or older\n"
     "- Family history of diabetes\n"
     "- Physical inactivity\n"
     "- History of gestational diabetes\n"
     "- Polycystic ovary syndrome (PCOS)\n"
     "- High blood pressure (above 140/90 mmHg)\n"
     "- Abnormal cholesterol levels"),

    ("Diagnosis",
     "Diabetes is diagnosed using several blood tests:\n"
     "- Fasting Plasma Glucose (FPG): Measures blood sugar after an overnight fast. A level of 126 mg/dL or higher indicates diabetes.\n"
     "- A1C Test (HbA1c): Measures average blood sugar over the past 2-3 months. An A1C of 6.5% or higher indicates diabetes.\n"
     "- Oral Glucose Tolerance Test (OGTT): Measures blood sugar 2 hours after drinking a glucose solution. A level of 200 mg/dL or higher indicates diabetes.\n"
     "- Random Plasma Glucose: A blood sugar of 200 mg/dL or higher with symptoms suggests diabetes."),

    ("Management and Treatment",
     "Type 1 Diabetes: Requires insulin therapy (injections or pump), blood sugar monitoring, carbohydrate counting, and regular exercise.\n\n"
     "Type 2 Diabetes: Management includes lifestyle changes (healthy diet, regular physical activity, weight management), blood sugar monitoring, and possibly oral medications or insulin.\n\n"
     "Key targets for management:\n"
     "- A1C below 7% for most adults\n"
     "- Fasting blood sugar: 80-130 mg/dL\n"
     "- Blood sugar 2 hours after meals: less than 180 mg/dL\n"
     "- Blood pressure below 140/90 mmHg"),

    ("Prevention of Type 2 Diabetes",
     "Type 2 diabetes can often be prevented or delayed through lifestyle changes:\n"
     "- Maintain a healthy weight\n"
     "- Get at least 150 minutes of moderate physical activity per week\n"
     "- Eat a balanced diet rich in fruits, vegetables, and whole grains\n"
     "- Limit sugar and refined carbohydrates\n"
     "- Avoid tobacco use\n"
     "- Get regular health screenings\n\n"
     "Studies show that lifestyle changes can reduce the risk of Type 2 diabetes by up to 58%."),

    ("Complications",
     "Uncontrolled diabetes can lead to serious complications:\n"
     "- Cardiovascular disease (heart attack, stroke)\n"
     "- Neuropathy (nerve damage causing numbness and pain)\n"
     "- Nephropathy (kidney damage potentially requiring dialysis)\n"
     "- Retinopathy (eye damage that can lead to blindness)\n"
     "- Foot problems (poor circulation leading to infections and amputation)\n"
     "- Skin conditions and infections\n"
     "- Hearing impairment\n"
     "- Alzheimer's disease association"),
])


# --- PDF 2: Hypertension Guide ---
create_pdf("Hypertension-Guide.pdf", "Understanding High Blood Pressure", [
    ("What is Hypertension?",
     "Hypertension, or high blood pressure, is a common condition in which the long-term force of blood against artery walls is high enough to eventually cause health problems such as heart disease. Blood pressure is determined by the amount of blood the heart pumps and the resistance to blood flow in the arteries. The more blood the heart pumps and the narrower the arteries, the higher the blood pressure."),

    ("Blood Pressure Categories",
     "Blood pressure readings consist of two numbers:\n"
     "- Systolic (top number): Pressure when the heart beats\n"
     "- Diastolic (bottom number): Pressure when the heart rests between beats\n\n"
     "Categories:\n"
     "- Normal: Less than 120/80 mmHg\n"
     "- Elevated: 120-129/less than 80 mmHg\n"
     "- Stage 1 Hypertension: 130-139/80-89 mmHg\n"
     "- Stage 2 Hypertension: 140+/90+ mmHg\n"
     "- Hypertensive Crisis: Higher than 180/120 mmHg (seek emergency care)"),

    ("Symptoms",
     "Hypertension is often called the 'silent killer' because most people with high blood pressure have no symptoms, even when blood pressure readings reach dangerously high levels. Some people may experience headaches, shortness of breath, or nosebleeds, but these signs are not specific and usually do not occur until blood pressure has reached a severe or life-threatening stage.\n\n"
     "Warning signs of hypertensive crisis include:\n"
     "- Severe headaches\n"
     "- Chest pain\n"
     "- Difficulty breathing\n"
     "- Vision problems\n"
     "- Blood in urine\n"
     "- Dizziness or fatigue"),

    ("Risk Factors",
     "Factors that increase the risk of hypertension:\n"
     "- Age (risk increases with age)\n"
     "- Family history of hypertension\n"
     "- Being overweight or obese\n"
     "- Physical inactivity\n"
     "- Tobacco use\n"
     "- High sodium diet (more than 2,300 mg/day)\n"
     "- Low potassium diet\n"
     "- Excessive alcohol consumption\n"
     "- Stress\n"
     "- Chronic conditions (kidney disease, diabetes, sleep apnea)"),

    ("Diagnosis and Monitoring",
     "Blood pressure is measured using a sphygmomanometer (blood pressure cuff). For an accurate diagnosis, blood pressure should be measured on at least two separate occasions. Ambulatory blood pressure monitoring (ABPM) or home monitoring may be recommended for confirmation.\n\n"
     "Tips for accurate readings:\n"
     "- Rest for 5 minutes before measurement\n"
     "- Sit with feet flat on the floor\n"
     "- Support your arm at heart level\n"
     "- Do not talk during measurement\n"
     "- Avoid caffeine, exercise, and smoking 30 minutes before"),

    ("Treatment and Management",
     "Lifestyle modifications (recommended for all patients):\n"
     "- DASH diet (Dietary Approaches to Stop Hypertension)\n"
     "- Reduce sodium intake to less than 2,300 mg/day (ideally 1,500 mg)\n"
     "- Regular physical activity (150 minutes of moderate exercise per week)\n"
     "- Maintain a healthy weight (BMI 18.5-24.9)\n"
     "- Limit alcohol (max 1 drink/day for women, 2 for men)\n"
     "- Quit smoking\n"
     "- Manage stress\n\n"
     "Medications may include:\n"
     "- ACE inhibitors\n"
     "- Angiotensin II receptor blockers (ARBs)\n"
     "- Calcium channel blockers\n"
     "- Diuretics\n"
     "- Beta-blockers"),

    ("Complications of Uncontrolled Hypertension",
     "Long-term uncontrolled high blood pressure can lead to:\n"
     "- Heart attack and heart failure\n"
     "- Stroke\n"
     "- Kidney disease or failure\n"
     "- Vision loss\n"
     "- Sexual dysfunction\n"
     "- Peripheral artery disease\n"
     "- Vascular dementia\n"
     "- Aneurysm"),
])


# --- PDF 3: Common Cold and Flu ---
create_pdf("Cold-and-Flu-Guide.pdf", "Common Cold and Influenza Guide", [
    ("Common Cold Overview",
     "The common cold is a viral infection of the upper respiratory tract (nose and throat). It is usually harmless, although it might not feel that way. Many types of viruses can cause a common cold, but rhinoviruses are the most common cause. Adults average 2-3 colds per year, while children may have even more."),

    ("Cold Symptoms",
     "Cold symptoms usually appear 1-3 days after exposure to a cold virus and may include:\n"
     "- Runny or stuffy nose\n"
     "- Sore throat\n"
     "- Cough\n"
     "- Sneezing\n"
     "- Mild body aches\n"
     "- Low-grade fever\n"
     "- Generally feeling unwell (malaise)\n\n"
     "Symptoms typically last 7-10 days. Nasal discharge may become thicker and yellow or green in color, which is normal and does not necessarily indicate a bacterial infection."),

    ("Influenza (Flu) Overview",
     "Influenza is a contagious respiratory illness caused by influenza viruses. It can cause mild to severe illness, and in some cases can lead to death. The flu is different from a cold. Flu symptoms are usually more intense and come on suddenly, while cold symptoms develop gradually.\n\n"
     "Flu season typically occurs in fall and winter, with activity peaking between December and February in the Northern Hemisphere."),

    ("Flu Symptoms",
     "Flu symptoms usually come on suddenly and may include:\n"
     "- High fever (100-104 F / 38-40 C)\n"
     "- Severe body aches and muscle pain\n"
     "- Chills and sweats\n"
     "- Headache\n"
     "- Dry, persistent cough\n"
     "- Extreme fatigue and weakness\n"
     "- Sore throat\n"
     "- Runny or stuffy nose\n"
     "- Vomiting and diarrhea (more common in children)\n\n"
     "Most people recover within 1-2 weeks, but some may develop complications."),

    ("When to Seek Medical Attention",
     "Seek medical care if you experience:\n"
     "- Difficulty breathing or shortness of breath\n"
     "- Persistent chest pain or pressure\n"
     "- Confusion or altered mental state\n"
     "- Severe or persistent vomiting\n"
     "- Flu-like symptoms that improve but then return with fever and worse cough\n"
     "- High fever lasting more than 3 days\n\n"
     "Emergency warning signs in children:\n"
     "- Fast or troubled breathing\n"
     "- Bluish skin color\n"
     "- Not drinking enough fluids\n"
     "- Not waking up or interacting\n"
     "- Fever with a rash"),

    ("Treatment",
     "Common Cold Treatment:\n"
     "- Rest and stay hydrated\n"
     "- Over-the-counter decongestants and pain relievers\n"
     "- Saline nasal spray\n"
     "- Warm liquids (tea, soup) to soothe throat\n"
     "- Honey for cough (not for children under 1 year)\n"
     "- Antibiotics are NOT effective against colds (they treat bacterial infections only)\n\n"
     "Flu Treatment:\n"
     "- Antiviral medications (oseltamivir/Tamiflu, zanamivir) if started within 48 hours\n"
     "- Rest and fluids\n"
     "- Over-the-counter medications for symptom relief\n"
     "- Stay home for at least 24 hours after fever breaks"),

    ("Prevention",
     "Cold Prevention:\n"
     "- Wash hands frequently with soap for at least 20 seconds\n"
     "- Avoid touching your face\n"
     "- Disinfect frequently touched surfaces\n"
     "- Avoid close contact with sick people\n\n"
     "Flu Prevention:\n"
     "- Annual flu vaccination (recommended for everyone 6 months and older)\n"
     "- Hand hygiene\n"
     "- Cover coughs and sneezes\n"
     "- Avoid crowded places during flu season\n"
     "- Maintain a healthy lifestyle (sleep, nutrition, exercise)"),
])


# --- PDF 4: Mental Health Basics ---
create_pdf("Mental-Health-Basics.pdf", "Mental Health: A Basic Guide", [
    ("What is Mental Health?",
     "Mental health includes emotional, psychological, and social well-being. It affects how we think, feel, and act. It also helps determine how we handle stress, relate to others, and make choices. Mental health is important at every stage of life, from childhood through adulthood.\n\n"
     "Good mental health is not just the absence of mental health problems. It means being able to cope with the normal stresses of life, work productively, and contribute to your community."),

    ("Common Mental Health Conditions",
     "Depression: A mood disorder causing persistent feelings of sadness and loss of interest. Symptoms include changes in sleep, appetite, energy level, concentration, and self-esteem. Depression affects more than 280 million people worldwide.\n\n"
     "Anxiety Disorders: A group of disorders characterized by excessive worry, fear, or nervousness. Types include generalized anxiety disorder (GAD), panic disorder, social anxiety disorder, and specific phobias.\n\n"
     "Post-Traumatic Stress Disorder (PTSD): Can develop after exposure to a traumatic event. Symptoms include flashbacks, nightmares, severe anxiety, and uncontrollable thoughts about the event.\n\n"
     "Bipolar Disorder: Characterized by extreme mood swings that include emotional highs (mania or hypomania) and lows (depression)."),

    ("Warning Signs",
     "Common warning signs of mental health problems include:\n"
     "- Feeling sad or withdrawn for more than 2 weeks\n"
     "- Severe mood swings\n"
     "- Excessive worry, fear, or anxiety\n"
     "- Social withdrawal\n"
     "- Changes in eating or sleeping habits\n"
     "- Difficulty concentrating\n"
     "- Loss of interest in activities once enjoyed\n"
     "- Low energy or fatigue\n"
     "- Feelings of hopelessness\n"
     "- Substance abuse\n"
     "- Thoughts of self-harm or suicide\n\n"
     "If you or someone you know is experiencing thoughts of suicide, contact emergency services or a crisis helpline immediately."),

    ("Treatment Options",
     "Mental health conditions are treatable. Common treatment approaches include:\n\n"
     "Psychotherapy (Talk Therapy):\n"
     "- Cognitive Behavioral Therapy (CBT)\n"
     "- Interpersonal Therapy (IPT)\n"
     "- Dialectical Behavior Therapy (DBT)\n\n"
     "Medications:\n"
     "- Antidepressants (SSRIs, SNRIs)\n"
     "- Anti-anxiety medications\n"
     "- Mood stabilizers\n"
     "- Antipsychotic medications\n\n"
     "Other approaches:\n"
     "- Support groups\n"
     "- Lifestyle changes (exercise, nutrition, sleep)\n"
     "- Mindfulness and meditation\n"
     "- Crisis intervention"),

    ("Self-Care for Mental Health",
     "Taking care of your mental health is just as important as physical health:\n"
     "- Get regular exercise (at least 30 minutes most days)\n"
     "- Maintain a regular sleep schedule (7-9 hours for adults)\n"
     "- Eat a balanced, nutritious diet\n"
     "- Stay connected with friends and family\n"
     "- Practice relaxation techniques (deep breathing, meditation)\n"
     "- Set realistic goals\n"
     "- Limit alcohol and avoid recreational drugs\n"
     "- Seek professional help when needed\n"
     "- Take breaks when feeling overwhelmed\n"
     "- Practice gratitude and positive thinking"),

    ("When to Seek Help",
     "You should consider seeking professional help if:\n"
     "- Symptoms interfere with daily activities or work\n"
     "- You are using alcohol or drugs to cope\n"
     "- You feel unable to manage your emotions\n"
     "- Symptoms persist for more than 2 weeks\n"
     "- You are having difficulty in relationships\n"
     "- You have thoughts of harming yourself or others\n\n"
     "Remember: Seeking help is a sign of strength, not weakness. Mental health conditions are medical conditions, just like heart disease or diabetes, and they respond to treatment."),
])


# --- PDF 5: First Aid Basics ---
create_pdf("First-Aid-Basics.pdf", "Basic First Aid Guide", [
    ("What is First Aid?",
     "First aid is the immediate care given to a person who has been injured or suddenly taken ill. It includes self-help and home care if medical assistance is not available or is delayed. First aid knowledge can mean the difference between life and death, between temporary and permanent disability, or between rapid recovery and prolonged hospitalization."),

    ("Basic First Aid Steps (DR ABC)",
     "When encountering an emergency, follow these steps:\n\n"
     "D - Danger: Check for danger to yourself and others before approaching\n"
     "R - Response: Check if the person is conscious. Tap their shoulder and ask 'Are you OK?'\n"
     "A - Airway: If unconscious, tilt the head back and lift the chin to open the airway\n"
     "B - Breathing: Look, listen, and feel for breathing for up to 10 seconds\n"
     "C - Circulation: If not breathing normally, call emergency services and begin CPR"),

    ("CPR (Cardiopulmonary Resuscitation)",
     "CPR is a life-saving technique used when someone's heart stops beating:\n\n"
     "For adults:\n"
     "1. Call emergency services (911/999/112)\n"
     "2. Place the heel of one hand on the center of the chest\n"
     "3. Place your other hand on top and interlock fingers\n"
     "4. Press down hard and fast (at least 2 inches deep)\n"
     "5. Compress at a rate of 100-120 compressions per minute\n"
     "6. If trained, give 2 rescue breaths after every 30 compressions\n"
     "7. Continue until emergency services arrive or the person starts breathing\n\n"
     "For infants (under 1 year): Use two fingers for compressions, press about 1.5 inches deep."),

    ("Choking",
     "Signs of choking include inability to talk, difficulty breathing, squeaky sounds, coughing, and skin turning blue.\n\n"
     "For conscious adults and children over 1 year (Heimlich Maneuver):\n"
     "1. Stand behind the person\n"
     "2. Make a fist with one hand, place it just above the navel\n"
     "3. Grasp your fist with the other hand\n"
     "4. Give quick, upward abdominal thrusts\n"
     "5. Repeat until the object is expelled or the person becomes unconscious\n\n"
     "For infants: Give 5 back blows followed by 5 chest thrusts. Do NOT perform abdominal thrusts on infants."),

    ("Bleeding and Wound Care",
     "For minor cuts and scrapes:\n"
     "1. Clean the wound with clean water\n"
     "2. Apply gentle pressure with a clean cloth to stop bleeding\n"
     "3. Apply antibiotic ointment\n"
     "4. Cover with a sterile bandage\n\n"
     "For severe bleeding:\n"
     "1. Call emergency services immediately\n"
     "2. Apply firm, direct pressure with a clean cloth\n"
     "3. If blood soaks through, add more layers (do not remove the first cloth)\n"
     "4. Elevate the injured area above heart level if possible\n"
     "5. Use a tourniquet only as a last resort for life-threatening limb bleeding"),

    ("Burns",
     "First-degree burns (red, no blisters): Cool under running water for at least 10 minutes. Apply aloe vera or moisturizer. Take over-the-counter pain relievers if needed.\n\n"
     "Second-degree burns (blisters, very painful): Cool under running water for at least 20 minutes. Do not pop blisters. Cover with a sterile non-stick bandage. Seek medical attention.\n\n"
     "Third-degree burns (charred, white or brown, may be painless): Call emergency services immediately. Do not apply water, ointments, or ice. Cover loosely with a sterile bandage. Monitor for shock.\n\n"
     "NEVER apply butter, toothpaste, or ice to burns."),

    ("When to Call Emergency Services",
     "Call emergency services (911/999/112) immediately for:\n"
     "- Chest pain or difficulty breathing\n"
     "- Stroke symptoms (face drooping, arm weakness, speech difficulty)\n"
     "- Severe bleeding that won't stop\n"
     "- Unconsciousness\n"
     "- Severe allergic reaction (anaphylaxis)\n"
     "- Suspected spinal injury\n"
     "- Seizures lasting more than 5 minutes\n"
     "- Poisoning or overdose\n"
     "- Severe burns\n"
     "- Head injuries with loss of consciousness"),
])


print(f"\n{'='*50}")
print(f"Created 5 sample PDFs in {KNOWLEDGE_BASE_DIR}")
print(f"{'='*50}")
