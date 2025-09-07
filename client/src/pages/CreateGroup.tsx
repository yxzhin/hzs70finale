import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import './CreateGroup.css';

function CreateGroup() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        name: ""
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        
        navigate('/create_group_func', { state: formData });
    };

    return (
        <div className="create-group">
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    placeholder="Enter the group name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                />
                <button type='submit'>Create</button>
            </form>
        </div>
    );
}

export default CreateGroup;