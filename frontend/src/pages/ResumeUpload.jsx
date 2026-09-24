import { useState } from "react";

import api from "../services/api";


function ResumeUpload({ user }) {

    const [file, setFile] = useState(null);

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const [resume, setResume] = useState(null);

    const [skills, setSkills] = useState([]);


    const handleFileChange = (event) => {

        const selectedFile = event.target.files[0];

        setFile(selectedFile);

        setMessage("");
        setError("");
    };


    const handleUpload = async (event) => {

        event.preventDefault();

        setMessage("");
        setError("");
        setResume(null);
        setSkills([]);


        if (!file) {

            setError(
                "Please select a resume file"
            );

            return;
        }


        if (!user) {

            setError(
                "User information is not available"
            );

            return;
        }


        const formData = new FormData();

        formData.append(
            "user_id",
            user.user_id
        );

        formData.append(
            "resume",
            file
        );


        try {

            const response = await api.post(
                "/resumes/upload",
                formData
            );


            setMessage(
                response.data.message
            );


            setResume(
                response.data.data
            );


            setFile(null);

            event.target.reset();


        } catch (error) {

            console.error(error);


            if (error.response) {

                setError(
                    error.response.data.message
                );

            } else {

                setError(
                    "Could not connect to backend"
                );

            }

        }

    };


    const handleExtractSkills = async () => {

        if (!resume) {

            setError(
                "Please upload a resume first"
            );

            return;
        }


        setMessage("");
        setError("");
        setSkills([]);


        try {

            const response = await api.post(
                `/resumes/${resume.resume_id}/extract-skills`
            );


            setMessage(
                response.data.message
            );


            setSkills(
                response.data.data.skills
            );


        } catch (error) {

            console.error(error);


            if (error.response) {

                setError(
                    error.response.data.message
                );

            } else {

                setError(
                    "Could not connect to backend"
                );

            }

        }

    };


    return (

        <div className="resume-page-content">


            {/* Upload Section */}

            <div className="resume-upload-box">

                <div className="resume-upload-icon">
                    📄
                </div>


                <h2>
                    Upload Your Resume
                </h2>


                <p>
                    Upload your resume in PDF or DOCX format
                    to extract your skills using NLP.
                </p>


                <form
                    onSubmit={handleUpload}
                    className="resume-form"
                >

                    <label className="file-upload-area">

                        <span className="file-icon">
                            📎
                        </span>

                        <span>
                            {file
                                ? file.name
                                : "Choose your resume"
                            }
                        </span>

                        <small>
                            PDF or DOCX
                        </small>


                        <input
                            type="file"
                            accept=".pdf,.docx"
                            onChange={handleFileChange}
                        />

                    </label>


                    <button
                        type="submit"
                        className="resume-upload-button"
                    >
                        Upload Resume
                    </button>

                </form>

            </div>


            {/* Messages */}

            {message && (

                <div className="resume-success">
                    ✓ {message}
                </div>

            )}


            {error && (

                <div className="resume-error">
                    ⚠ {error}
                </div>

            )}


            {/* Uploaded Resume */}

            {resume && (

                <div className="resume-result-card">

                    <div className="resume-result-header">

                        <div>

                            <span className="result-file-icon">
                                📄
                            </span>

                            <div>

                                <h3>
                                    Resume Uploaded
                                </h3>

                                <p>
                                    {resume.file_name}
                                </p>

                            </div>

                        </div>


                        <span className="resume-id">
                            ID: {resume.resume_id}
                        </span>

                    </div>


                    <button
                        className="extract-button"
                        onClick={handleExtractSkills}
                    >
                        🔍 Extract Skills
                    </button>


                    <div className="resume-text-section">

                        <h3>
                            Extracted Resume Text
                        </h3>


                        <div className="resume-text-box">

                            {resume.extracted_text}

                        </div>

                    </div>

                </div>

            )}


            {/* Skills */}

            {skills.length > 0 && (

                <div className="skills-card">

                    <h3>
                        🧠 Detected Skills
                    </h3>


                    <p>
                        Skills identified from your resume
                    </p>


                    <div className="skills-container">

                        {skills.map(
                            (skill, index) => (

                                <span
                                    className="skill-tag"
                                    key={index}
                                >
                                    {skill}
                                </span>

                            )
                        )}

                    </div>

                </div>

            )}

        </div>

    );

}


export default ResumeUpload;