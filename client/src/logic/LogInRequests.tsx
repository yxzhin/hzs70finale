import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";

interface LogInData {
    name: string;
    password: string;
}

function LogInRequest() {
    const location = useLocation();
    const navigate = useNavigate();
    const data = location.state as LogInData;

    const hasFetched = useRef(false);
    
    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;
    
        if (!data?.name || !data?.password) {
            navigate("/sign_in?error=empty", { replace: true });
            return;
        }
    
            fetch("http://localhost:5000/user/login", {
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
                    if (result?.token && result?.user?.id) {
                        localStorage.setItem('jwt', result['token']);
                        localStorage.setItem('userid', result['user']['id']);
                        navigate(`/dashboard`, { replace: true });
                    } else {
                        navigate("/sign_in?error=invalid_response", { replace: true });
                    }
                })
                .catch(err => {
                    console.error("Registration error:", err);
                    navigate("/sign_in?error=server", { replace: true });
                });
        }, [data, navigate]);

    return <p>Awaiting server response</p>;
}

export default LogInRequest;