function JobCard({employer, title, expirationDate, location, source}) {
  return (
    <div className="Job-card">
      <h3>{employer}</h3>
      <p><strong>Type:</strong> {title}</p>
      <p><strong>Lokasjon:</strong> {location}</p>
      <p><strong>Utgår:</strong> {expirationDate}</p>
      <p><strong>Kilde:</strong> {source}</p>
    </div>
  );
}

export default JobCard;