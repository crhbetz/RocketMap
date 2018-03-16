$(function () {
    'use strict'
    Store.set('showWeatherCells', false)
    Store.set('showWeatherAlerts', false)
    Store.set('showS2Cells', false)

    const totalExcluded = Store.get('remember_select_exclude') // Retrieve what has already been set.
    const excludedPokemon = [10, 13, 16, 17, 19, 20, 21, 29, 32, 41, 46, 48, 122, 161, 162, 163, 165, 166, 177, 187, 188, 190, 194, 198, 263, 265, 273, 276, 293, 299, 300, 311, 312, 313, 315, 316] // Add Pokémon IDs separated by commas (e.g. [1, 2, 3])

    // If the new default Pokémon doesn't exist then add it to the list.
    excludedPokemon.forEach((id) => {
         if (totalExcluded.indexOf(id) === -1) {
             totalExcluded.push(id)
         }
    })

    Store.set('remember_select_exclude', totalExcluded)
})
