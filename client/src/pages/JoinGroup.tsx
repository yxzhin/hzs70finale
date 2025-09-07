import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import './JoinGroup.css';

function JoinGroup() {
    const groupId = new URLSearchParams(window.location.search).get("group");
    const [groupName, setGroupName] = useState('');

    const navigate = useNavigate();
    const [toRedirect, setToRedirect] = useState(false);

    const token = localStorage.getItem('jwt');

    if (!token) {
        useEffect(() => {
            navigate('/signup', { replace: true });
        })
    }
    else {
        const hasFetched = useRef(false);
            
        useEffect(() => {
            if (hasFetched.current) return;
            hasFetched.current = true;
        
            fetch("http://localhost:5000/user/current_user", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(async (res) => {
                if (res.status == 404) {
                    return;
                } else if (res.status == 500) {
                    localStorage.setItem('jwt', '');
                    window.location.reload();
                } else if (res.status == 200) {
                } else {
                    throw new Error(`Unexpected status: ${res.status}`);
                }
            })
            .catch(err => {
                console.error("Registration error:", err);
                navigate("/signup?error=server", { replace: true });
            });
        }, [navigate]);
    }

    useEffect(() => {
        if (toRedirect)
            return;

        if (groupId === null) {
            setToRedirect(true);
            return;
        }

        fetch(`http://localhost:5000/groups/${groupId}`, {
            method: 'GET'
        })
        .then(async (res) => {
            if (res.status === 404 || res.status === 500) {
                setToRedirect(true);
                return;
            }

            if (res.status !== 200) {
                setToRedirect(true);
                console.error(`Invalid result status: ${res.status}`);
                return;
            }
            
            const data = await res.json();
            setGroupName(data['name']);
        })
    }, [groupId]);

    useEffect(() => {
        if (!toRedirect) return;
        const timer = setTimeout(() => {
            navigate("/");
        }, 5000);
        return () => clearTimeout(timer);
    }, [toRedirect, navigate]);

    if (toRedirect) {
        return <h1>Invalid link, redirecting in a few seconds...</h1>;
    }

    const handleClick = () => {
        fetch(`http://localhost:5000/user_groups/${groupId}`, {
            method: 'POST',
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }).then(async (res) => {
            if (res.status !== 200) {
                console.error(`Invalid status code: ${res.status}`);
            }

            navigate('/', { replace: true });
        })
    }

    return (
        <div className="invite">
            <h1>You are invited into {groupName}</h1>
            <button onClick={handleClick} className="primary-btn">Accept</button>
        </div>
    );
}


export default JoinGroup;