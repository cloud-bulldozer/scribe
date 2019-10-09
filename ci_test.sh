#!/bin/bash

# Prep the results.markdown file
echo "Results for "$JOB_NAME > results.markdown
echo "" >> results.markdown
echo 'Module | Pass/Fail' >> results.markdown
echo '-----|-------|' >> results.markdown

# Clone and prep Stockpile
git clone https://github.com/cloud-bulldozer/stockpile.git

cp stockpile/ci/all.yml stockpile/group_vars/all.yml

# It's redundant to run it against kubernetes hosts atm so we remove them from the
# hosts file
cat stockpile/ci/hosts | grep -v ^# | sed -e '/\[kubernetes\]/,+1d' > stockpile/hosts

sed -i 's/\/tmp\/stockpile.json/\/tmp\/stockpile_scribe.json/' stockpile/group_vars/all.yml

cd stockpile

echo "Running Stockpile"
ansible-playbook -i hosts stockpile.yml -e kube_config=/root/.kube/config #--skip-tags=backpack_kube

cd ..

module_list=`ls transcribe/scribe_modules/*.py | grep -v __ | grep -v base_scribe_module | sed 's/.py//' | awk -F "/" '{print $3}'`

echo "Scribe module list: "$module_list

# Create python3 virt env for the test
python3 -m venv ci_test

source ci_test/bin/activate

# Install scribe into the venv
pip3 install -e .

rc=0

python3 -m scribe -t stockpile -ip /tmp/stockpile_scribe.json > scribe_out
scribe_rc=$?

if [[ $scribe_rc -eq 1 ]]
then
  echo "Scribe failed to run. Exiting"
  exit 1
fi

echo "Full scribe output:"
cat scribe_out
echo ""
echo ""
echo ""
echo "Scribe Module Results:"

for module in $module_list
do
  grep $module" is not part" scribe_out
  my_rc=$?

  if [ $my_rc -eq 1 ]
  then
    echo $module": Passed"
    echo $module"|Pass" >> results.markdown
  else
    echo $module": Failed"
    echo $module"|Fail" >> results.markdown
    rc=1
  fi
done

deactivate

rm -rf stockpile ci_test 

exit $rc
