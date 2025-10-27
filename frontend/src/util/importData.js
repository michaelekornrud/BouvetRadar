import { useState, useEffect } from 'react';

const pathBackendApi = `http://localhost:8080/api`;

function CPVCategorieNamesList() {
    const [codes, setCodes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`${pathBackendApi}/cpv/categories`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setCodes(data.data);
                setLoading(false);
            })
            .catch(error => {
                setError(error.message);
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Laster...</div>;
    if (error) return <div>Feil: {error}</div>;

    return (
        <div className='Filter-options'>
            {codes.map(option => (
                AddOptionWithCheckbox(option)
            ))}
        </div>
    );
}

function AddOptionWithCheckbox(option){
    return (
        <div className='Option'>
            <input type='checkbox' id={option.code}/> <p>{option.description}</p>
        </div>
    );
}

export default CPVCategorieNamesList;