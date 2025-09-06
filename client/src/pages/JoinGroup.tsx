import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import './JoinGroup.css';

function JoinGroup() {
    const decodeId = (encoded: string): number | null => {
        const scrambled = parseInt(encoded, 12);
        if (isNaN(scrambled)) return null;
        return scrambled ^ 123456;
    };

    const groupCode = new URLSearchParams(window.location.search).get("group");
    const groupId = groupCode ? decodeId(groupCode) : null;
    const [groupName, setGroupName] = useState('');

    const navigate = useNavigate();
    const [toRedirect, setToRedirect] = useState(false);

    useEffect(() => {
        if (groupId === null) {
            setToRedirect(true);
            return;
        }

        fetch(`http://localhost:5000/groups/${groupId}/`, {
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

    return (
        <div className="invite">
            <h1>You are invited into {groupName}</h1>
            <a href={`/accept_invite?group=${groupCode}`}>
                <button className="primary-btn">Accept</button>
            </a>
        </div>
    );
}


export default JoinGroup;