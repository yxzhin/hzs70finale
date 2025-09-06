import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

function Success() {
    const navigate = useNavigate();
    const token = localStorage.getItem('jwt');

    if (!token) {
        navigate('/', { replace: true });
    }

    const [userId, setUserId] = useState<number | null>(null);

    const [loading, setLoading] = useState(true);
    const [isAuthorized, setIsAuthorized] = useState(false);

    const fetchedId = useRef(false);

    useEffect(() => {
        if (fetchedId.current) return;
        fetchedId.current = true;

        if (!token) {
            navigate("/sign_in", { replace: true });
            return;
        }

        fetch("http://localhost:5000/user/current_user", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        })
        .then(async (res) => {
            if (res.status === 404) {
                navigate("/", { replace: true });
            } else if (res.status === 500) {
                localStorage.setItem("jwt", "");
                window.location.reload();
            } else if (res.status === 200) {
                const data = await res.json();
                setUserId(data.id);
                setIsAuthorized(true);
            } else {
                throw new Error(`Unexpected status: ${res.status}`);
            }
        })
        .catch(err => {
            console.error("Registration error:", err);
            navigate("/sign_in", { replace: true });
        })
        .finally(() => {
            setLoading(false);
        });
    }, [token, navigate]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (!isAuthorized) {
        return null;
    }

    return (
        <div className="success-page">
            <h1>Registration Successful!</h1>
            <p>Your user ID is: {userId}</p>
            <p>You can now log in with your credentials.</p>
        </div>
    );
}

export default Success;