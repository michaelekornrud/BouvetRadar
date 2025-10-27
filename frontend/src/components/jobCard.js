function JobCard({employer, title, expirationDate, location, source}) {
  return (
    <div className="Job-card">
      <h2>{employer}</h2>
      <p>Title: {title}</p>
      <p>Location: {location}</p>
      <p>Expires on: {expirationDate}</p>
      <p>Source: {source}</p>
    </div>
  );
}

export default JobCard;