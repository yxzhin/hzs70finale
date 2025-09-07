import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";

interface GroupData {
    name: string;
}

function CreateGroupFunc() {
    const location = useLocation();
    const navigate = useNavigate();
    const data = location.state as GroupData;

    const token = localStorage.getItem('jwt');
    useEffect(() => {
        if (!token) navigate('/', { replace: true });
    }, [token, navigate]);

    const fetched = useRef(false);

    useEffect(() => {
        if (fetched.current) return;
        fetched.current = true;
        
        fetch("http://localhost:5000/user/current_user", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })
        .then(async (res) => {
            if (res.status == 404) {
                navigate('/', { replace: true });
            } else if (res.status == 500) {
                localStorage.setItem('jwt', '');
                navigate('/', { replace: true });
            } else if (res.status == 200) {
                const result = await res.json();
            } else {
                throw new Error(`Unexpected status: ${res.status}`);
            }
        })
        .catch(err => {
            console.error("Registration error:", err);
            navigate("/signup?error=server", { replace: true });
        });
    }, [token, navigate]);

    const hasFetched = useRef(false);
    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;
         
        if (!data?.name) {
            navigate("/create_group?error=empty", { replace: true });
            return;
        }
     
        fetch("http://localhost:5000/groups/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                name: data.name
            })
        })
        .then(async (_) => {
            navigate('/dashboard');
        })
        .catch(err => {
            console.error("Registration error:", err);
            navigate("/sign_up?error=server", { replace: true });
        });
    }, [data, navigate]);

    return <p>Submitting your registration...</p>;
}

export default CreateGroupFunc;