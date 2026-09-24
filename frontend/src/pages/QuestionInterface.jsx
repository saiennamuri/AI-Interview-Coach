import { useState } from "react";

import api from "../services/api";


function QuestionInterface({ interview }) {

    const [questions, setQuestions] = useState([]);

    const [currentIndex, setCurrentIndex] = useState(0);

    const [answer, setAnswer] = useState("");

    const [message, setMessage] = useState("");

    const [error, setError] = useState("");

    const [loading, setLoading] = useState(false);

    const [submitted, setSubmitted] = useState(false);

    const [evaluation, setEvaluation] = useState(null);

    const [evaluating, setEvaluating] = useState(false);


    /* ============================= */
    /* Generate Questions */
    /* ============================= */

    const generateQuestions = async () => {

        setMessage("");
        setError("");
        setQuestions([]);
        setCurrentIndex(0);
        setAnswer("");
        setSubmitted(false);
        setEvaluation(null);
        setLoading(true);


        try {

            const response = await api.post(
                `/interviews/${interview.interview_id}/generate-questions`
            );


            setMessage(
                response.data.message
            );


            setQuestions(
                response.data.data.questions
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

        } finally {

            setLoading(false);

        }
    };


    /* ============================= */
    /* Submit Answer */
    /* ============================= */

    const submitAnswer = async () => {

        setMessage("");
        setError("");


        if (!answer.trim()) {

            setError(
                "Please enter your answer"
            );

            return;
        }


        try {

            const response = await api.post(
                `/interviews/questions/${questions[currentIndex].question_id}/answer`,
                {
                    answer_text: answer
                }
            );


            setMessage(
                response.data.message
            );


            setSubmitted(true);


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


    /* ============================= */
    /* Evaluate Answer */
    /* ============================= */

    const evaluateAnswer = async () => {

        setMessage("");
        setError("");


        if (!submitted) {

            setError(
                "Please submit your answer first"
            );

            return;
        }


        setEvaluating(true);


        try {

            const response = await api.post(
                `/interviews/questions/${questions[currentIndex].question_id}/evaluate`
            );


            setEvaluation(
                response.data.data
            );


            setMessage(
                response.data.message
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

        } finally {

            setEvaluating(false);

        }
    };


    /* ============================= */
    /* Next Question */
    /* ============================= */

    const nextQuestion = () => {

        if (
            currentIndex <
            questions.length - 1
        ) {

            setCurrentIndex(
                currentIndex + 1
            );

            setAnswer("");

            setMessage("");

            setError("");

            setSubmitted(false);

            setEvaluation(null);
        }
    };


    /* ============================= */
    /* Previous Question */
    /* ============================= */

    const previousQuestion = () => {

        if (currentIndex > 0) {

            setCurrentIndex(
                currentIndex - 1
            );

            setAnswer("");

            setMessage("");

            setError("");

            setSubmitted(false);

            setEvaluation(null);
        }
    };


    /* ============================= */
    /* No Interview */
    /* ============================= */

    if (!interview) {

        return (

            <div className="question-empty">

                <div className="empty-icon">
                    🎤
                </div>

                <h2>
                    No Interview Selected
                </h2>

                <p>
                    Please create an interview before
                    starting your AI interview.
                </p>

            </div>

        );
    }


    const currentQuestion =
        questions[currentIndex];


    const progress =
        questions.length > 0
            ? ((currentIndex + 1) / questions.length) * 100
            : 0;


    return (

        <div className="question-interface">


            {/* ============================= */}
            {/* Interview Header */}
            {/* ============================= */}

            <div className="question-header">

                <div className="question-header-icon">
                    🎤
                </div>


                <div>

                    <p className="question-header-label">
                        AI MOCK INTERVIEW
                    </p>

                    <h1>
                        {interview.job_role}
                    </h1>

                    <p>
                        Answer the questions and get
                        AI-powered feedback.
                    </p>

                </div>

            </div>


            {/* ============================= */}
            {/* Interview Information */}
            {/* ============================= */}

            <div className="interview-info-row">

                <div className="info-badge">

                    <span>
                        🎯
                    </span>

                    <div>
                        <small>
                            Difficulty
                        </small>

                        <strong>
                            {interview.difficulty}
                        </strong>
                    </div>

                </div>


                <div className="info-badge">

                    <span>
                        💼
                    </span>

                    <div>
                        <small>
                            Interview Type
                        </small>

                        <strong>
                            {interview.interview_type}
                        </strong>

                    </div>

                </div>


                {questions.length > 0 && (

                    <div className="info-badge">

                        <span>
                            📋
                        </span>

                        <div>

                            <small>
                                Progress
                            </small>

                            <strong>
                                {currentIndex + 1} / {questions.length}
                            </strong>

                        </div>

                    </div>

                )}

            </div>


            {/* ============================= */}
            {/* Generate Questions */}
            {/* ============================= */}

            {questions.length === 0 && (

                <div className="generate-card">

                    <div className="generate-icon">
                        ✨
                    </div>


                    <h2>
                        Ready to Start?
                    </h2>


                    <p>
                        Generate personalized interview
                        questions based on your selected
                        job role and difficulty.
                    </p>


                    <button
                        className="generate-button"
                        onClick={generateQuestions}
                        disabled={loading}
                    >

                        {loading ? (
                            <>
                                <span className="button-spinner"></span>
                                Generating Questions...
                            </>
                        ) : (
                            <>
                                ✨ Generate Questions
                            </>
                        )}

                    </button>

                </div>

            )}


            {/* ============================= */}
            {/* Question Area */}
            {/* ============================= */}

            {questions.length > 0 && currentQuestion && (

                <div className="question-section">


                    {/* Progress */}

                    <div className="progress-section">

                        <div className="progress-label">

                            <span>
                                Question {currentIndex + 1}
                                {" "}of{" "}
                                {questions.length}
                            </span>

                            <span>
                                {Math.round(progress)}%
                            </span>

                        </div>


                        <div className="progress-bar">

                            <div
                                className="progress-fill"
                                style={{
                                    width: `${progress}%`
                                }}
                            ></div>

                        </div>

                    </div>


                    {/* Question Card */}

                    <div className="question-card">

                        <div className="question-card-top">

                            <span className="question-number">
                                Q{currentIndex + 1}
                            </span>


                            <div className="question-tags">

                                <span className="question-type-tag">
                                    {currentQuestion.question_type}
                                </span>


                                <span className="question-difficulty-tag">
                                    {currentQuestion.difficulty}
                                </span>

                            </div>

                        </div>


                        <h2 className="question-text">

                            {currentQuestion.question_text}

                        </h2>

                    </div>


                    {/* Answer Section */}

                    <div className="answer-card">

                        <div className="answer-header">

                            <div>

                                <h3>
                                    💬 Your Answer
                                </h3>

                                <p>
                                    Explain your answer clearly
                                    and include relevant examples
                                    when possible.
                                </p>

                            </div>

                        </div>


                        <textarea
                            className="answer-textarea"
                            value={answer}
                            onChange={(event) =>
                                setAnswer(event.target.value)
                            }
                            placeholder="Type your answer here..."
                            disabled={submitted}
                        />


                        <div className="answer-footer">

                            <span>
                                {answer.length} characters
                            </span>


                            <div className="answer-actions">

                                <button
                                    className="submit-answer-button"
                                    onClick={submitAnswer}
                                    disabled={submitted}
                                >

                                    {submitted
                                        ? "✓ Answer Submitted"
                                        : "Submit Answer"
                                    }

                                </button>


                                <button
                                    className="evaluate-button"
                                    onClick={evaluateAnswer}
                                    disabled={
                                        !submitted ||
                                        evaluating
                                    }
                                >

                                    {evaluating
                                        ? "Evaluating..."
                                        : "🤖 Evaluate Answer"
                                    }

                                </button>

                            </div>

                        </div>

                    </div>


                    {/* Messages */}

                    {message && (

                        <div className="question-success">
                            ✓ {message}
                        </div>

                    )}


                    {error && (

                        <div className="question-error">
                            ⚠ {error}
                        </div>

                    )}


                    {/* ============================= */}
                    {/* Evaluation */}
                    {/* ============================= */}

                    {evaluation && (

                        <div className="evaluation-section">

                            <div className="evaluation-header">

                                <div className="evaluation-icon">
                                    🤖
                                </div>

                                <div>

                                    <p>
                                        AI ANALYSIS
                                    </p>

                                    <h2>
                                        Answer Evaluation
                                    </h2>

                                </div>

                            </div>


                            <div className="score-grid">


                                <div className="score-card">

                                    <span>
                                        🎯
                                    </span>

                                    <small>
                                        Relevance
                                    </small>

                                    <strong>
                                        {evaluation.scores.relevance_score}
                                    </strong>

                                    <em>
                                        / 100
                                    </em>

                                </div>


                                <div className="score-card">

                                    <span>
                                        🔑
                                    </span>

                                    <small>
                                        Keywords
                                    </small>

                                    <strong>
                                        {evaluation.scores.keyword_score}
                                    </strong>

                                    <em>
                                        / 100
                                    </em>

                                </div>


                                <div className="score-card">

                                    <span>
                                        🧠
                                    </span>

                                    <small>
                                        Semantic
                                    </small>

                                    <strong>
                                        {evaluation.scores.semantic_score}
                                    </strong>

                                    <em>
                                        / 100
                                    </em>

                                </div>


                                <div className="score-card">

                                    <span>
                                        ✨
                                    </span>

                                    <small>
                                        Clarity
                                    </small>

                                    <strong>
                                        {evaluation.scores.clarity_score}
                                    </strong>

                                    <em>
                                        / 100
                                    </em>

                                </div>

                            </div>


                            {/* Overall Score */}

                            <div className="overall-score-card">

                                <div>

                                    <span className="overall-label">
                                        OVERALL SCORE
                                    </span>

                                    <h2>
                                        {evaluation.scores.overall_score}
                                        <small>
                                            / 100
                                        </small>
                                    </h2>

                                </div>


                                <div className="score-message">

                                    {evaluation.scores.overall_score >= 85
                                        ? "Excellent answer! 🌟"
                                        : evaluation.scores.overall_score >= 70
                                            ? "Good answer! 👍"
                                            : evaluation.scores.overall_score >= 50
                                                ? "Fair answer. Keep improving! 💪"
                                                : "Keep practicing! 🚀"
                                    }

                                </div>

                            </div>


                            {/* Feedback */}

                            <div className="feedback-card">

                                <div className="feedback-icon">
                                    💡
                                </div>


                                <div>

                                    <h3>
                                        AI Feedback
                                    </h3>

                                    <p>
                                        {evaluation.feedback}
                                    </p>

                                </div>

                            </div>

                        </div>

                    )}


                    {/* ============================= */}
                    {/* Navigation */}
                    {/* ============================= */}

                    <div className="question-navigation">

                        <button
                            className="nav-button previous"
                            onClick={previousQuestion}
                            disabled={currentIndex === 0}
                        >
                            ← Previous
                        </button>


                        <span>
                            {currentIndex + 1} / {questions.length}
                        </span>


                        <button
                            className="nav-button next"
                            onClick={nextQuestion}
                            disabled={
                                currentIndex ===
                                questions.length - 1
                            }
                        >
                            Next →
                        </button>

                    </div>

                </div>

            )}

        </div>
    );
}


export default QuestionInterface;

