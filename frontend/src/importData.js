import { useState, useEffect } from 'react';

function CPVCategoriesList() {
    const [codes, setCodes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('http://10.99.40.111:8080/api/cpv/categories')
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
        <div>
            {codes.map(code => (
                <div key={code.code}>
                    <h3>{code.code}</h3>
                    <p>{code.description}</p>
                </div>
            ))}
        </div>
    );
}

export default CPVCategoriesList;