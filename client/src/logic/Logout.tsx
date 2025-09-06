import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Logout() {
    const navigate = useNavigate();

    useEffect(() => {
        localStorage.setItem('jwt', '');
        localStorage.setItem('userid', '');
        navigate("/", { replace: true });
    }, [navigate]);

    return (
        <p>Logging out...</p>
    );
}

export default Logout;