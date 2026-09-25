const API_URL = "http://127.0.0.1:8000";


// Load dashboard data
async function loadDashboard() {

    try {

        // Get students
        const studentsResponse = await fetch(
            `${API_URL}/students/`
        );

        const students = await studentsResponse.json();

        document.getElementById("studentCount").textContent =
            students.length;


        // Get subjects
        const subjectsResponse = await fetch(
            `${API_URL}/subjects/`
        );

        const subjects = await subjectsResponse.json();

        document.getElementById("subjectCount").textContent =
            subjects.length;


        // Get attendance
        const attendanceResponse = await fetch(
            `${API_URL}/attendance/`
        );

        const attendance = await attendanceResponse.json();

        document.getElementById("attendanceCount").textContent =
            attendance.length;

    } catch (error) {

        console.error("Error loading dashboard:", error);

    }
}


// Get student attendance report
async function getReport() {

    const studentId =
        document.getElementById("studentId").value;

    if (!studentId) {
        alert("Please enter Student ID");
        return;
    }

    try {

        // Attendance report
        const reportResponse = await fetch(
            `${API_URL}/attendance/report/${studentId}`
        );

        const report = await reportResponse.json();


        if (!reportResponse.ok) {

            document.getElementById("reportResult").innerHTML =
                `<p>${report.detail}</p>`;

            return;
        }


        document.getElementById("reportResult").innerHTML = `

            <p>
                <strong>Total Classes:</strong>
                ${report.total_classes}
            </p>

            <p>
                <strong>Present:</strong>
                ${report.present}
            </p>

            <p>
                <strong>Absent:</strong>
                ${report.absent}
            </p>

            <p>
                <strong>Attendance:</strong>
                ${report.attendance_percentage}%
            </p>

        `;


        // Attendance analysis
        const analysisResponse = await fetch(
            `${API_URL}/attendance/analysis/${studentId}`
        );

        const analysis = await analysisResponse.json();


        document.getElementById("analysisResult").innerHTML = `

            <p>
                <strong>Attendance:</strong>
                ${analysis.attendance_percentage}%
            </p>

            <p>
                <strong>Analysis:</strong>
                ${analysis.analysis}
            </p>

        `;

    } catch (error) {

        console.error("Error:", error);

        document.getElementById("reportResult").innerHTML =
            "<p>Unable to connect to the server.</p>";
    }
}


// Run dashboard when page opens
loadDashboard();