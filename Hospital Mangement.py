import os
import json
from datetime import datetime

import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Hospital Management System",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: bold;
        color: #1565C0;
    }

    .section-title {
        font-size: 25px;
        font-weight: bold;
        color: #1976D2;
    }

    .doctor-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
        background-color: #f8fbff;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GROQ API CONFIGURATION
# ============================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("GROQ_API_KEY is not configured.")
    st.info(
        "Add GROQ_API_KEY in Streamlit Cloud → "
        "Settings → Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)


# ============================================================
# INITIALIZE PATIENT DATA
# ============================================================

if "patients" not in st.session_state:
    st.session_state.patients = [
        {
            "id": "P001",
            "name": "Rahul Kumar",
            "age": 35,
            "gender": "Male",
            "phone": "9876543210",
            "blood_group": "O+",
            "history": "No major history reported",
            "allergies": "None reported",
            "past_visits": [
                {
                    "date": "2026-07-15",
                    "department": "General Medicine",
                    "doctor": "Dr. Anil Kumar",
                    "symptoms": "Fever and tiredness",
                    "notes": "Routine follow-up advised"
                }
            ]
        },
        {
            "id": "P002",
            "name": "Priya Sharma",
            "age": 29,
            "gender": "Female",
            "phone": "9876501234",
            "blood_group": "A+",
            "history": "Seasonal allergy reported",
            "allergies": "Dust",
            "past_visits": [
                {
                    "date": "2026-06-21",
                    "department": "General Medicine",
                    "doctor": "Dr. Anil Kumar",
                    "symptoms": "Cold and cough",
                    "notes": "Follow-up completed"
                }
            ]
        }
    ]


# ============================================================
# INITIALIZE DOCTOR DATA
# ============================================================

if "doctors" not in st.session_state:
    st.session_state.doctors = [
        {
            "id": "D001",
            "name": "Dr. Anil Kumar",
            "specialization": "General Medicine",
            "department": "General Medicine",
            "experience": "12 years",
            "availability": "Monday - Friday, 9:00 AM - 1:00 PM"
        },
        {
            "id": "D002",
            "name": "Dr. Priya Sharma",
            "specialization": "Cardiology",
            "department": "Cardiology",
            "experience": "15 years",
            "availability": "Monday - Saturday, 10:00 AM - 2:00 PM"
        },
        {
            "id": "D003",
            "name": "Dr. Ravi Reddy",
            "specialization": "Neurology",
            "department": "Neurology",
            "experience": "10 years",
            "availability": "Tuesday - Saturday, 11:00 AM - 3:00 PM"
        },
        {
            "id": "D004",
            "name": "Dr. Sneha Rao",
            "specialization": "Pediatrics",
            "department": "Pediatrics",
            "experience": "8 years",
            "availability": "Monday - Friday, 9:00 AM - 1:00 PM"
        },
        {
            "id": "D005",
            "name": "Dr. Arjun Singh",
            "specialization": "Orthopedics",
            "department": "Orthopedics",
            "experience": "11 years",
            "availability": "Monday - Saturday, 2:00 PM - 6:00 PM"
        },
        {
            "id": "D006",
            "name": "Dr. Meera Nair",
            "specialization": "Dermatology",
            "department": "Dermatology",
            "experience": "9 years",
            "availability": "Monday - Friday, 10:00 AM - 2:00 PM"
        },
        {
            "id": "D007",
            "name": "Dr. Karthik Rao",
            "specialization": "ENT",
            "department": "ENT",
            "experience": "13 years",
            "availability": "Tuesday - Saturday, 9:00 AM - 1:00 PM"
        },
        {
            "id": "D008",
            "name": "Dr. Divya Patel",
            "specialization": "Gynecology",
            "department": "Gynecology",
            "experience": "14 years",
            "availability": "Monday - Saturday, 11:00 AM - 4:00 PM"
        },
        {
            "id": "D009",
            "name": "Dr. Vikram Shah",
            "specialization": "Pulmonology",
            "department": "Pulmonology",
            "experience": "10 years",
            "availability": "Monday - Friday, 2:00 PM - 6:00 PM"
        },
        {
            "id": "D010",
            "name": "Dr. Neha Verma",
            "specialization": "Psychiatry",
            "department": "Psychiatry",
            "experience": "7 years",
            "availability": "Monday - Friday, 10:00 AM - 3:00 PM"
        }
    ]


# ============================================================
# INITIALIZE APPOINTMENTS
# ============================================================

if "appointments" not in st.session_state:
    st.session_state.appointments = [
        {
            "appointment_id": "A001",
            "patient": "Rahul Kumar",
            "patient_id": "P001",
            "doctor": "Dr. Anil Kumar",
            "doctor_id": "D001",
            "department": "General Medicine",
            "date": "2026-08-15",
            "time": "10:00 AM",
            "status": "Confirmed"
        }
    ]


# ============================================================
# INITIALIZE AI REQUESTS
# ============================================================

if "ai_requests" not in st.session_state:
    st.session_state.ai_requests = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_doctors_by_department(department):
    """
    Find doctors whose department matches
    the requested department.
    """
    matches = []

    for doctor in st.session_state.doctors:
        if doctor["department"].lower() == department.lower():
            matches.append(doctor)

    return matches


def get_patient_by_id(patient_id):
    """
    Find a patient by ID.
    """
    for patient in st.session_state.patients:
        if patient["id"].lower() == patient_id.lower():
            return patient

    return None


def generate_patient_id():
    """
    Generate the next patient ID.
    """
    number = len(st.session_state.patients) + 1
    return f"P{number:03d}"


def generate_appointment_id():
    """
    Generate the next appointment ID.
    """
    number = len(st.session_state.appointments) + 1
    return f"A{number:03d}"


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏥 Hospital Management")

st.sidebar.write(
    "AI-powered hospital administration demo"
)

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Patient Registration",
        "Patient Past Data",
        "Doctors & Specializations",
        "AI Health Chatbot",
        "Doctor Appointments"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "AI output is for demonstration and "
    "administrative decision support only."
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">'
        '🏥 AI Hospital Management Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Central dashboard for patients, doctors, "
        "AI review requests and appointments."
    )

    st.divider()

    total_patients = len(
        st.session_state.patients
    )

    total_doctors = len(
        st.session_state.doctors
    )

    total_appointments = len(
        st.session_state.appointments
    )

    pending_requests = len(
        [
            request
            for request in st.session_state.ai_requests
            if request["status"] == "Pending Doctor Review"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👤 Patients",
            total_patients
        )

    with col2:
        st.metric(
            "👨‍⚕️ Doctors",
            total_doctors
        )

    with col3:
        st.metric(
            "📅 Appointments",
            total_appointments
        )

    with col4:
        st.metric(
            "🤖 Pending AI Reviews",
            pending_requests
        )

    st.divider()

    st.subheader("📅 Recent Appointments")

    if st.session_state.appointments:

        st.dataframe(
            st.session_state.appointments,
            use_container_width=True
        )

    else:

        st.info(
            "No appointments available."
        )

    st.divider()

    st.subheader(
        "🤖 Pending Doctor Review Requests"
    )

    pending = [
        request
        for request in st.session_state.ai_requests
        if request["status"] == "Pending Doctor Review"
    ]

    if pending:

        st.dataframe(
            pending,
            use_container_width=True
        )

    else:

        st.success(
            "No pending doctor review requests."
        )


# ============================================================
# PATIENT REGISTRATION
# ============================================================

elif page == "Patient Registration":

    st.title("👤 Patient Registration")

    st.write(
        "Register a new patient in the hospital system."
    )

    with st.form("patient_registration_form"):

        col1, col2 = st.columns(2)

        with col1:

            patient_name = st.text_input(
                "Patient Name"
            )

            patient_age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=18
            )

            patient_gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Other"
                ]
            )

            patient_phone = st.text_input(
                "Phone Number"
            )

        with col2:

            blood_group = st.selectbox(
                "Blood Group",
                [
                    "A+",
                    "A-",
                    "B+",
                    "B-",
                    "AB+",
                    "AB-",
                    "O+",
                    "O-"
                ]
            )

            medical_history = st.text_area(
                "Medical History"
            )

            allergies = st.text_area(
                "Allergies"
            )

        submit_patient = st.form_submit_button(
            "Register Patient",
            type="primary"
        )

        if submit_patient:

            if not patient_name.strip():

                st.warning(
                    "Please enter the patient name."
                )

            else:

                new_patient = {
                    "id": generate_patient_id(),
                    "name": patient_name,
                    "age": patient_age,
                    "gender": patient_gender,
                    "phone": patient_phone,
                    "blood_group": blood_group,
                    "history": medical_history,
                    "allergies": allergies,
                    "past_visits": []
                }

                st.session_state.patients.append(
                    new_patient
                )

                st.success(
                    f"Patient registered successfully. "
                    f"Patient ID: {new_patient['id']}"
                )


# ============================================================
# PATIENT PAST DATA
# ============================================================

elif page == "Patient Past Data":

    st.title("📋 Patient Past Data")

    st.write(
        "Search and view a patient's previous hospital records."
    )

    patient_search = st.text_input(
        "Search Patient",
        placeholder="Enter patient name or patient ID"
    )

    if patient_search:

        search_text = patient_search.lower()

        matching_patients = [
            patient
            for patient in st.session_state.patients
            if (
                search_text in patient["name"].lower()
                or search_text in patient["id"].lower()
            )
        ]

        if matching_patients:

            for patient in matching_patients:

                st.subheader(
                    f"👤 {patient['name']} "
                    f"({patient['id']})"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"**Age:** {patient['age']}"
                    )

                    st.write(
                        f"**Gender:** {patient['gender']}"
                    )

                    st.write(
                        f"**Phone:** {patient['phone']}"
                    )

                with col2:

                    st.write(
                        f"**Blood Group:** "
                        f"{patient['blood_group']}"
                    )

                    st.write(
                        f"**Medical History:** "
                        f"{patient['history']}"
                    )

                with col3:

                    st.write(
                        f"**Allergies:** "
                        f"{patient['allergies']}"
                    )

                st.markdown(
                    "### 🩺 Previous Visits"
                )

                if patient["past_visits"]:

                    st.dataframe(
                        patient["past_visits"],
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No previous visits recorded."
                    )

                st.divider()

        else:

            st.warning(
                "No patient found."
            )


# ============================================================
# DOCTORS & SPECIALIZATIONS
# ============================================================

elif page == "Doctors & Specializations":

    st.title("👨‍⚕️ Doctors & Specializations")

    st.write(
        "View doctors, departments, specializations, "
        "experience and availability."
    )

    departments = [
        "All Departments"
    ]

    for doctor in st.session_state.doctors:

        if doctor["department"] not in departments:

            departments.append(
                doctor["department"]
            )

    selected_department = st.selectbox(
        "Filter by Department",
        departments
    )

    if selected_department == "All Departments":

        filtered_doctors = (
            st.session_state.doctors
        )

    else:

        filtered_doctors = [
            doctor
            for doctor in st.session_state.doctors
            if doctor["department"]
            == selected_department
        ]

    st.metric(
        "Doctors Available",
        len(filtered_doctors)
    )

    st.divider()

    for doctor in filtered_doctors:

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [2, 2, 2]
            )

            with col1:

                st.subheader(
                    f"👨‍⚕️ {doctor['name']}"
                )

                st.write(
                    f"**Doctor ID:** "
                    f"{doctor['id']}"
                )

            with col2:

                st.write(
                    f"**Specialization:** "
                    f"{doctor['specialization']}"
                )

                st.write(
                    f"**Department:** "
                    f"{doctor['department']}"
                )

            with col3:

                st.write(
                    f"**Experience:** "
                    f"{doctor['experience']}"
                )

                st.write(
                    f"**Availability:** "
                    f"{doctor['availability']}"
                )


# ============================================================
# AI HEALTH CHATBOT
# ============================================================

elif page == "AI Health Chatbot":

    st.title("🤖 AI Health Chatbot")

    st.warning(
        "This AI does not provide a definitive medical "
        "diagnosis or prescribe treatment. It organizes "
        "patient information and identifies whether "
        "professional medical review should be requested."
    )

    st.write(
        "Enter the patient's symptoms and relevant information."
    )

    col1, col2 = st.columns(2)

    with col1:

        patient_name = st.text_input(
            "Patient Name"
        )

    with col2:

        patient_id = st.text_input(
            "Patient ID",
            placeholder="Example: P001"
        )

    symptoms = st.text_area(
        "Current Symptoms",
        height=150,
        placeholder=(
            "Describe the symptoms, when they started, "
            "and other relevant information."
        )
    )

    additional_information = st.text_area(
        "Additional Information",
        height=130,
        placeholder=(
            "Medical history, allergies, recent tests, "
            "existing conditions, etc."
        )
    )

    analyze_button = st.button(
        "🤖 Analyze & Request Doctor Review",
        type="primary"
    )

    if analyze_button:

        if not patient_name.strip():

            st.warning(
                "Please enter the patient name."
            )

        elif not symptoms.strip():

            st.warning(
                "Please enter the patient's symptoms."
            )

        else:

            ai_prompt = f"""
You are an AI hospital administrative
and patient-triage assistant.

You are NOT a doctor.

Review the information below and organize
it for a qualified healthcare professional.

PATIENT:
{patient_name}

PATIENT ID:
{patient_id}

CURRENT SYMPTOMS:
{symptoms}

ADDITIONAL INFORMATION:
{additional_information}

RULES:

1. Do not provide a definitive diagnosis.
2. Do not prescribe medication.
3. Do not create a treatment plan.
4. Do not invent patient information.
5. Identify possible areas of concern only.
6. State that a qualified healthcare professional
   must make the final diagnosis.
7. Determine whether professional medical review
   should be requested.
8. If the information indicates potentially urgent
   symptoms, clearly mark the urgency as Urgent.
9. Choose a hospital department from this list:

General Medicine
Cardiology
Neurology
Pediatrics
Orthopedics
Dermatology
ENT
Gynecology
Pulmonology
Psychiatry

Return ONLY valid JSON in this exact format:

{{
    "summary": "short summary",
    "possible_concerns": [
        "concern 1",
        "concern 2"
    ],
    "doctor_review_required": true,
    "urgency": "Routine",
    "recommended_department": "General Medicine",
    "reason_for_review": "short explanation"
}}
"""

            with st.spinner(
                "AI is analyzing the information..."
            ):

                try:

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a cautious "
                                    "hospital administrative "
                                    "AI assistant. Never "
                                    "claim to diagnose patients."
                                )
                            },
                            {
                                "role": "user",
                                "content": ai_prompt
                            }
                        ],
                        response_format={
                            "type": "json_object"
                        },
                        temperature=0.1
                    )

                    ai_response = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    analysis = json.loads(
                        ai_response
                    )

                    st.session_state.last_analysis = analysis

                    st.success(
                        "AI review completed."
                    )

                    st.subheader(
                        "📋 AI Review Summary"
                    )

                    st.write(
                        analysis.get(
                            "summary",
                            "No summary available."
                        )
                    )

                    st.markdown(
                        "### 🔎 Possible Concerns"
                    )

                    concerns = analysis.get(
                        "possible_concerns",
                        []
                    )

                    if concerns:

                        for concern in concerns:

                            st.markdown(
                                f"- {concern}"
                            )

                    else:

                        st.write(
                            "No concerns were identified "
                            "from the provided information."
                        )

                    urgency = analysis.get(
                        "urgency",
                        "Routine"
                    )

                    st.markdown(
                        "### 🚦 Review Priority"
                    )

                    if urgency.lower() == "urgent":

                        st.error(
                            "🚨 Urgent professional "
                            "medical review may be required."
                        )

                    elif urgency.lower() == "soon":

                        st.warning(
                            "⚠️ Professional medical "
                            "review should be arranged soon."
                        )

                    else:

                        st.info(
                            "ℹ️ Routine professional "
                            "medical review may be appropriate."
                        )

                    department = analysis.get(
                        "recommended_department",
                        "General Medicine"
                    )

                    st.markdown(
                        f"### 🏥 Recommended Department: "
                        f"{department}"
                    )

                    review_required = analysis.get(
                        "doctor_review_required",
                        False
                    )

                    if review_required:

                        matched_doctors = (
                            find_doctors_by_department(
                                department
                            )
                        )

                        if not matched_doctors:

                            matched_doctors = (
                                find_doctors_by_department(
                                    "General Medicine"
                                )
                            )

                        request = {
                            "request_id": (
                                f"R{len(st.session_state.ai_requests) + 1:03d}"
                            ),
                            "patient": patient_name,
                            "patient_id": patient_id,
                            "department": department,
                            "urgency": urgency,
                            "reason": analysis.get(
                                "reason_for_review",
                                "Professional review requested."
                            ),
                            "requested_at": datetime.now().strftime(
                                "%Y-%m-%d %H:%M"
                            ),
                            "status": "Pending Doctor Review"
                        }

                        if matched_doctors:

                            request["suggested_doctor"] = (
                                matched_doctors[0]["name"]
                            )

                            request["doctor_id"] = (
                                matched_doctors[0]["id"]
                            )

                        else:

                            request["suggested_doctor"] = (
                                "Doctor To Be Assigned"
                            )

                            request["doctor_id"] = "N/A"

                        st.session_state.ai_requests.append(
                            request
                        )

                        st.success(
                            "👨‍⚕️ Doctor review request "
                            "has been created."
                        )

                        st.subheader(
                            "📅 Doctor Review Request"
                        )

                        st.write(
                            f"**Patient:** "
                            f"{request['patient']}"
                        )

                        st.write(
                            f"**Department:** "
                            f"{request['department']}"
                        )

                        st.write(
                            f"**Suggested Doctor:** "
                            f"{request['suggested_doctor']}"
                        )

                        st.write(
                            f"**Priority:** "
                            f"{request['urgency']}"
                        )

                        st.info(
                            "The hospital staff can confirm "
                            "the doctor and appointment time "
                            "from the Doctor Appointments page."
                        )

                    else:

                        st.info(
                            "No doctor appointment request "
                            "was created from the provided information."
                        )

                except json.JSONDecodeError:

                    st.error(
                        "The AI returned an invalid response. "
                        "Please try again."
                    )

                except Exception as error:

                    st.error(
                        "Unable to connect to the AI service."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# DOCTOR APPOINTMENTS
# ============================================================

elif page == "Doctor Appointments":

    st.title("📅 Doctor Appointments")

    st.write(
        "Review AI-generated requests and assign "
        "a suitable doctor."
    )

    st.divider()

    # --------------------------------------------------------
    # AI REQUESTS
    # --------------------------------------------------------

    st.subheader(
        "🤖 AI Doctor Review Requests"
    )

    pending_requests = [
        request
        for request in st.session_state.ai_requests
        if request["status"] == "Pending Doctor Review"
    ]

    if pending_requests:

        for request in pending_requests:

            with st.container(border=True):

                st.write(
                    f"### 👤 {request['patient']}"
                )

                st.write(
                    f"**Patient ID:** "
                    f"{request['patient_id']}"
                )

                st.write(
                    f"**Department:** "
                    f"{request['department']}"
                )

                st.write(
                    f"**Priority:** "
                    f"{request['urgency']}"
                )

                st.write(
                    f"**Reason:** "
                    f"{request['reason']}"
                )

                st.write(
                    f"**Suggested Doctor:** "
                    f"{request['suggested_doctor']}"
                )

                # Find doctors for this department

                department_doctors = (
                    find_doctors_by_department(
                        request["department"]
                    )
                )

                if not department_doctors:

                    department_doctors = (
                        st.session_state.doctors
                    )

                doctor_options = [
                    (
                        doctor["name"]
                        + " - "
                        + doctor["specialization"]
                    )
                    for doctor in department_doctors
                ]

                selected_doctor_label = st.selectbox(
                    "Select Doctor",
                    doctor_options,
                    key=f"doctor_{request['request_id']}"
                )

                selected_doctor = None

                for doctor in department_doctors:

                    label = (
                        doctor["name"]
                        + " - "
                        + doctor["specialization"]
                    )

                    if label == selected_doctor_label:

                        selected_doctor = doctor
                        break

                col1, col2 = st.columns(2)

                with col1:

                    appointment_date = st.date_input(
                        "Appointment Date",
                        key=f"date_{request['request_id']}"
                    )

                with col2:

                    appointment_time = st.time_input(
                        "Appointment Time",
                        key=f"time_{request['request_id']}"
                    )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✅ Confirm Appointment",
                        key=f"confirm_{request['request_id']}",
                        type="primary"
                    ):

                        appointment = {
                            "appointment_id": (
                                generate_appointment_id()
                            ),
                            "patient": request["patient"],
                            "patient_id": request["patient_id"],
                            "doctor": selected_doctor["name"],
                            "doctor_id": selected_doctor["id"],
                            "department": selected_doctor["department"],
                            "date": str(appointment_date),
                            "time": appointment_time.strftime(
                                "%I:%M %p"
                            ),
                            "status": "Confirmed"
                        }

                        st.session_state.appointments.append(
                            appointment
                        )

                        request["status"] = (
                            "Confirmed"
                        )

                        request["assigned_doctor"] = (
                            selected_doctor["name"]
                        )

                        st.success(
                            "Appointment confirmed successfully."
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "❌ Reject Request",
                        key=f"reject_{request['request_id']}"
                    ):

                        request["status"] = (
                            "Rejected"
                        )

                        st.warning(
                            "Doctor review request rejected."
                        )

                        st.rerun()

    else:

        st.success(
            "No pending AI doctor review requests."
        )

    st.divider()

    # --------------------------------------------------------
    # ALL APPOINTMENTS
    # --------------------------------------------------------

    st.subheader(
        "📋 Hospital Appointment List"
    )

    if st.session_state.appointments:

        st.dataframe(
            st.session_state.appointments,
            use_container_width=True
        )

    else:

        st.info(
            "No appointments available."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏥 AI Hospital Management System | "
    "Demo application | "
    "AI output is not a medical diagnosis and "
    "must be reviewed by a qualified healthcare professional."
)