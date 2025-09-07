import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";

interface GroupData {
    name: string;
}

function CreateGroupFunc() {
    const location = useLocation();
    const navigate = useNavigate();
    const data = location.state as GroupData;

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
                "Content-Type": "application/json"
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