class Upppdf < Formula
  desc "Unlock password protected PDF files using multiple methods"
  homepage "https://github.com/abozaralizadeh/UPPPDF"
  url "https://github.com/abozaralizadeh/UPPPDF/archive/refs/tags/master.tar.gz"
  sha256 "d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed"
  license "MIT"

  head "https://github.com/abozaralizadeh/UPPPDF.git", branch: "master"

  depends_on "python@3.11"

  def install
    system "python3", "-m", "pip", "install", *std_pip_args, "."
  end

  test do
    system "#{bin}/upppdf", "--help"
  end
end