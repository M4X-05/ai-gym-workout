import streamlit as st
import openai
from fpdf import FPDF

# ✅ Ensure OpenAI API key is securely stored in Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ✅ Streamlit UI
st.title("💪 AI Workout Plan Generator")
st.subheader("Enter your details to get a structured workout plan!")

# ✅ User Inputs
goal = st.selectbox("🎯 Fitness Goal", ["Muscle Gain", "Fat Loss", "Endurance", "Strength", "General Fitness"])
experience = st.selectbox("🏋️ Experience Level", ["Beginner", "Intermediate", "Advanced"])
frequency = st.slider("📅 Workout Days Per Week", 1, 7, 4)
equipment = st.multiselect("🏋️‍♂️ Available Equipment", ["Gym", "Dumbbells", "Resistance Bands", "Bodyweight Only"])

# ✅ Generate Workout Plan
if st.button("Generate Workout Plan"):
    if not equipment:
        st.warning("⚠️ Please select at least one type of equipment.")
    else:
        equipment_list = ", ".join(equipment)

        # ✅ Improved AI Prompt
        prompt = f"""
        Create a structured {frequency}-day workout plan for a {experience} individual aiming for {goal}. 
        The user has access to {equipment_list}. Ensure the plan includes:

        - ✅ **Exercises per day** (specific names)
        - ✅ **Sets & reps**
        - ✅ **Rest times**
        - ✅ **Progression for 4 weeks** (how to increase weight, intensity)
        - ✅ **Warm-ups & cool-downs**
        - ✅ **Recovery & stretching**
        - ✅ **Nutrition guidance for {goal}**

        Format the response as a **weekly schedule** with clear headings.
        """

        # ✅ OpenAI API Call (Updated for OpenAI v1.0.0+)
        with st.spinner("Generating workout plan... ⏳"):
            try:
                response = openai.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800
                )
                workout_plan = response.choices[0].message.content
                st.success("✅ Here is your personalized workout plan:")
                st.text_area("Workout Plan", workout_plan, height=400)

                # ✅ Store in session state for history
                if "workout_history" not in st.session_state:
                    st.session_state.workout_history = []
                st.session_state.workout_history.append(workout_plan)

            except Exception as e:
                st.error(f"🚨 Error: {e}")

# ✅ Display Workout History
st.subheader("📜 Your Saved Workouts")
if "workout_history" in st.session_state:
    for i, plan in enumerate(st.session_state.workout_history):
        st.text_area(f"Workout {i+1}", plan, height=200)

# ✅ Alternative PDF Download (Replaces pdfkit)
def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(190, 10, content)
    return pdf

if "workout_plan" in locals():
    if st.button("📥 Download Workout Plan as PDF"):
        pdf = generate_pdf(workout_plan)
        pdf_output = "workout_plan.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as pdf_file:
            st.download_button("📥 Download PDF", pdf_file, file_name="Workout_Plan.pdf", mime="application/pdf")