function addQueryParam() {
  var queryParamDiv = document.getElementById("query-params");
  var newQueryParam = document.createElement("div");
  newQueryParam.className = "row g-2 mb-2 query-param";
  newQueryParam.innerHTML = '<div class="col-md-6 px-1"><div class="form-floating"><input type="text" class="form-control param-label" name="param-label" required><label for="floatingInputGrid" class="text-black">Query parameter</label></div></div><div class="col-md-5 px-1"><div class="form-floating"><input type="text" class="form-control param-value" name="param-value" required><label for="floatingInputGrid" class="text-black">Param Value</label></div></div><div class="col-md-1 d-flex justify-content-center align-items-center"><button type="button" class="btn btn-danger" onclick="removeQueryParam(this)">x</button></div>';
  queryParamDiv.appendChild(newQueryParam);
}


function removeQueryParam(paramRow) {
  const queryParams = document.getElementById("query-params");
  if (queryParams.children.length > 1) {
      queryParams.removeChild(paramRow.parentNode.parentNode);
  }
}