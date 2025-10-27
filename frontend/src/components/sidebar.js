import CPVCategorieNamesList from '../util/importData.js'

function FilterSideBar() {
    return (
        <div className="Filter">
            <h2>Filter</h2>
            <CPVCategorieNamesList/>
        </div>
    )
}

export default FilterSideBar;