export const estimateTokens = (str: string): number => {
  return Math.ceil(str.length / 2);
};

const truncateString = (str: string, truncateBy: number): string => {
  return str.slice(0, -truncateBy);
};

const truncateArray = (arr: any[], truncateBy: number): any[] => {
  // slice a random index in the array
  const randomIndex = Math.floor(Math.random() * arr.length);
  arr.splice(randomIndex, truncateBy);
  return arr;
};

const handleArray = (arr: any[], truncateBy: number): any[] => {
  const reducedArray = arr.map((item) => {
    if (typeof item === 'object' && estimateTokens(JSON.stringify(item)) > 20) {
      return truncateJson(item, truncateBy);
    } else if (typeof item === 'string') {
      return truncateString(item, truncateBy);
    } else {
      return item;
    }
  });

  // if the nothing changed in the reducedArray delete a random item from the array
  if (JSON.stringify(reducedArray) === JSON.stringify(arr)) {
    return truncateArray(arr, truncateBy);
  } else {
    return reducedArray;
  }
};

const truncateJson = (json: any, truncateBy: number): any => {
  if (typeof json === 'string') {
    return truncateString(json, truncateBy);
  } else if (Array.isArray(json)) {
    return handleArray(json, truncateBy);
  } else if (typeof json === 'object') {
    // ensure keys can get deleted
    let hasDeletedMisc = false;
    for (let key in json) {
      // if null or empty object, delete
      if (
        !json[key] ||
        (typeof json[key] === 'object' && Object.keys(json[key]).length === 0)
      ) {
        delete json[key];
        continue;
      }

      // if not string, array, or object, delete. Also delete if empty string or empty array
      if (
        !hasDeletedMisc &&
        (typeof json[key] !== 'string' ||
          (typeof json[key] === 'string' && !json[key].length)) &&
        (!Array.isArray(json[key]) ||
          (Array.isArray(json[key]) && !json[key].length)) &&
        typeof json[key] !== 'object'
      ) {
        hasDeletedMisc = true;
        delete json[key];
      } else {
        json[key] = truncateJson(json[key], truncateBy);
      }
    }
    if (Object.keys(json).length === 0) {
      return null; // remove empty objects
    }
    return json;
  } else {
    return json;
  }
};

export const truncateJsonRoot = (
  json: any,
  truncateTo: number,
  verbose = false
): any => {
  if (verbose)
    console.log(
      'original json token count: ' + estimateTokens(JSON.stringify(json))
    );
  let truncateBy = 1; // adjust this value as needed
  let prevJson;
  while (estimateTokens(JSON.stringify(json)) > truncateTo) {
    prevJson = JSON.stringify(json);
    json = truncateJson(json, truncateBy);
    if (JSON.stringify(json) === prevJson) {
      console.log('Failed to complete truncation.');
      break; // break out of the loop if truncateJson is not able to make any changes
    }
  }
  if (verbose)
    console.log(
      'final json token count: ' + estimateTokens(JSON.stringify(json))
    );
  return json;
};
