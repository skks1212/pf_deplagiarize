const verdicts = require('./verdicts.json');

    const toCheck = Object.values(verdicts).filter(
        v => v.percent < 90 && v.percent !== 0
    )

    function getKeyByValue(object, value) {
        return Object.keys(object).find(key => object[key] === value);
      }
    
    console.log(typeof toCheck)
    toCheck.forEach(v => {
        const key = getKeyByValue(verdicts, v);
        console.log(key);
    })