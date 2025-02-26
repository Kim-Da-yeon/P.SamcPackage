#' Run SAMC Simulation using Python Code via reticulate
#'
#' 이 함수는 inst/extdata 폴더에 저장된 SAMC.py 파이썬 코드를 불러와 실행합니다.
#' SAMC.py 파일 내에는 run_simulation() 함수가 정의되어 있어야 합니다.
#'
#' @return run_simulation()의 실행 결과를 반환합니다.
#' @export
run_samc_simulation <- function() {
  if (!requireNamespace("reticulate", quietly = TRUE)) {
    install.packages("reticulate")
  }
  library(reticulate)

  # 패키지 내부 inst/extdata 폴더에서 SAMC.py 파일 경로 가져오기
  py_file <- system.file("extdata", "SAMC.py", package = "P.SamcPackage")
  if (py_file == "") {
    stop("SAMC.py 파일이 inst/extdata 폴더에 없습니다.")
  }

  # SAMC.py 파일의 파이썬 코드를 불러옵니다.
  source_python(py_file)

  # SAMC.py 내에 run_simulation() 함수가 정의되어 있다고 가정합니다.
  result <- run_simulation()
  return(result)
}
