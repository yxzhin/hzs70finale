import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useRef } from "react";

interface SignUpData {
    name: string;
    password: string;
    passwordConfirm: string;
}

function SignUpRequest() {
    const location = useLocation();
    const navigate = useNavigate();
    const data = location.state as SignUpData;

    const hasFetched = useRef(false);

    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;

        if (!data?.name || !data?.password || !data?.passwordConfirm) {
            navigate("/signup?error=empty", { replace: true });
            return;
        }

        if (data.password !== data.passwordConfirm) {
            navigate("/signup?error=pwdnomatch", { replace: true });
            return;
        }

        fetch("http://localhost:5000/api/user/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: data.name,
                password: data.password
            })
        })
            .then(res => res.json())
            .then(result => {
                console.log("Server response:", result);
                localStorage.setItem('jwt', result['token']);
                localStorage.setItem('userid', result['user']['id']);
                navigate("/dashboard", { replace: true });
            })
            .catch(err => {
                console.error("Registration error:", err);
                navigate("/sign_up?error=server", { replace: true });
            });
    }, [data, navigate]);

    return <p>Submitting your registration...</p>;
}

export default SignUpRequest;