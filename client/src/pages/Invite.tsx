import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import './Invite.css';

function Invite() {
    const navigate = useNavigate();

    const groupId = Number(new URLSearchParams(window.location.search).get('id')) || 0;
    const [groupName, setGroupName] = useState('');

    useEffect(() => {
        fetch(`http://localhost:5000/groups/${groupId}`, {
            method: 'GET'
        }).then(async (res) => {
            if (res.status !== 200) {
                navigate('/', { replace: true });
                return;
            }
            const data = await res.json();
            setGroupName(data.name);
        })
    });

    const inviteLink = `${window.location.origin}/join?group=${groupId}`;

    const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?data=${encodeURIComponent(inviteLink)}&size=200x200`;

    useEffect(() => {
        fetch(`http://localhost:5000/groups/${groupId}`, {
            method: 'GET'
        })
        .then(async (res) => {
            const data = await res.json();

            if (res.status !== 200) {
                console.error(`Unknown status: ${res.status}`);
                navigate('/', { replace: true });
                return;
            }

            setGroupName(data.name);
        })
    })

    return (
        <div className="invite-page">
            <div className="invite-contents">
                <h1>Invite people to:<br/><span className='red-text'>{groupName}</span></h1>

                <div className="invite-methods">
                    <div className="invite-method lside-methods">
                        <h2>Share this link:</h2>
                        <input 
                            type="text"
                            readOnly
                            value={inviteLink}
                            className="invite-link"
                            onClick={(e) => (e.target as HTMLInputElement).select()}
                        />
                    </div>

                    <div className="invite-method rside-methods">
                        <h2>Or use a QR code:</h2>
                        <img src={qrCodeUrl} alt="QR Code" className="qr-code" />
                    </div>
                </div>
            </div>
            
        </div>
    );
}

export default Invite;