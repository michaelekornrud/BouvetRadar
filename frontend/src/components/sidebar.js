import CPVCategorieNamesList from '../util/importData.js'

function FilterSideBar() {
    const [cpvCategories] = CPVCategorieNamesList();

    return (
        <div className="Filter-sidebar">            
            <h2>Filter</h2>
            <div className='Filter-options'>
            {
                cpvCategories.map(option =>                
                    <div className='Option' key={option.code}>
                        <input type='checkbox' id={option.code} /> <p>{option.description}</p>
                    </div>
            )}
            </div>
        </div>
    )
}

export default FilterSideBar;